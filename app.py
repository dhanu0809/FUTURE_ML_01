import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pickle
from groq import Groq

st.set_page_config(
    page_title="Sales & Demand Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales & Demand Forecasting")
st.markdown("### AI-Powered Business Insights")
st.markdown("---")

@st.cache_resource
def load_model():
    with open('sales_forecast_model.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_stores():
    stores = pd.read_csv('stores.csv')
    stores.columns = stores.columns.str.strip().str.lower()
    return stores

@st.cache_data
def load_existing_data():
    df = pd.read_csv('forecast_results.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

model = load_model()
stores = load_stores()

st.sidebar.title("Settings")
api_key = st.secrets.get("GROQ_API_KEY", None)

st.sidebar.markdown("---")
st.sidebar.markdown("### Data Source")

option = st.sidebar.radio(
    "Choose Data Source",
    ["Use Existing Forecast Data", "Upload New Dataset"]
)

def process_data(df):
    df.columns = df.columns.str.strip().str.lower()

    if 'id' in df.columns:
        df = df.drop(columns=['id'])
    if 'sales' in df.columns:
        df = df.drop(columns=['sales'])

    required = ['store_nbr', 'family', 'date', 'onpromotion']
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Your CSV is missing required column(s): {missing}")
        st.stop()

    if 'type' not in df.columns or 'cluster' not in df.columns:
        df = df.merge(stores, on='store_nbr', how='left')

    unknown_stores = df[df['type'].isna()]['store_nbr'].unique()
    if len(unknown_stores) > 0:
        st.warning(
            f"Store(s) {list(unknown_stores)} not found in database "
            f"and will be excluded from predictions."
        )
        df = df.dropna(subset=['type', 'cluster'])

    if df.empty:
        st.error("No valid stores found. Please check your store numbers.")
        st.stop()

    if df['onpromotion'].min() < 0:
        st.warning("onpromotion column contains negative values — clipped to 0 automatically.")
        df['onpromotion'] = df['onpromotion'].clip(lower=0)

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    df['quarter'] = df['date'].dt.quarter
    df['type_encoded'] = df['type'].map({'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5})
    df['family_encoded'] = df['family'].astype('category').cat.codes

    features = ['store_nbr', 'family_encoded', 'onpromotion',
                'year', 'month', 'day', 'day_of_week',
                'week_of_year', 'is_weekend', 'quarter',
                'type_encoded', 'cluster']

    df['predicted_sales'] = model.predict(df[features]).clip(min=0)
    return df


if option == "Use Existing Forecast Data":
    df = load_existing_data()
    st.success("Loaded existing forecast data!")
    existing_csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download This Dataset",
        data=existing_csv,
        file_name="forecast_results.csv",
        mime="text/csv"
    )

else:
    st.sidebar.markdown("### Upload CSV")
    sample_template = pd.DataFrame({
        'store_nbr': [20, 50, 49],
        'family': ['BOOKS', 'DAIRY', 'BEVERAGES'],
        'date': ['2024-06-01', '2024-06-01', '2024-06-01'],
        'onpromotion': [1, 2, 0]
    })
    sample_csv = sample_template.to_csv(index=False)
    st.sidebar.download_button(
        label="Download Sample Template CSV",
        data=sample_csv,
        file_name="sample_sales_template.csv",
        mime="text/csv"
    )
    uploaded_file = st.sidebar.file_uploader(
        "Upload your sales CSV",
        type=['csv']
    )
    if uploaded_file is None:
        st.info("Upload a CSV file from the sidebar to get started")
        st.markdown("### Required CSV Format")
        st.markdown("Your file must contain exactly these 4 columns:")
        st.dataframe(sample_template)
        st.markdown("Store type, cluster, city and state are added automatically from our stores database.")
        st.stop()
    else:
        raw_df = pd.read_csv(uploaded_file)
        st.success(f"File uploaded — {len(raw_df)} rows loaded!")
        with st.spinner("Processing data and generating predictions..."):
            df = process_data(raw_df)

st.sidebar.markdown("---")
st.sidebar.markdown("### Filter Results")

years = sorted(df['year'].unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", years)

if 'type' in df.columns:
    store_types = ['All'] + sorted(df['type'].dropna().unique().tolist())
    selected_type = st.sidebar.selectbox("Select Store Type", store_types)
else:
    selected_type = 'All'

filtered_df = df[df['year'] == selected_year]
if selected_type != 'All':
    filtered_df = filtered_df[filtered_df['type'] == selected_type]

if filtered_df.empty:
    st.warning("No data available for this filter combination.")
    st.stop()

st.markdown(f"### Results — Year {selected_year} | Store Type {selected_type}")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Predicted Sales", f"{filtered_df['predicted_sales'].sum():,.0f}")
with col2:
    st.metric("Average Per Store", f"{filtered_df['predicted_sales'].mean():,.0f}")
with col3:
    top_store = filtered_df.groupby('store_nbr')['predicted_sales'].sum().idxmax()
    st.metric("Top Store", f"Store {top_store}")
with col4:
    top_cat = filtered_df.groupby('family')['predicted_sales'].sum().idxmax()
    st.metric("Top Category", top_cat)

st.markdown("---")

st.markdown("### Monthly Sales Trend")
monthly = filtered_df.groupby('month')['predicted_sales'].sum().reset_index()
monthly['month_name'] = pd.to_datetime(monthly['month'], format='%m').dt.strftime('%B')
fig1 = px.line(monthly, x='month_name', y='predicted_sales',
               title=f'Monthly Sales Trend ({selected_year})',
               markers=True, color_discrete_sequence=['#2196F3'])
st.plotly_chart(fig1, width='stretch')

st.markdown("### Sales by Store")
store_sales = filtered_df.groupby('store_nbr')['predicted_sales'].sum().reset_index()
fig2 = px.bar(store_sales, x='store_nbr', y='predicted_sales',
              title=f'Predicted Sales by Store ({selected_year})',
              color='predicted_sales', color_continuous_scale='Blues')
st.plotly_chart(fig2, width='stretch')

st.markdown("### Top Product Categories")
cat_sales = filtered_df.groupby('family')['predicted_sales'].sum().sort_values(
    ascending=False).head(10).reset_index()
fig3 = px.bar(cat_sales, x='family', y='predicted_sales',
              title=f'Top 10 Categories ({selected_year})',
              color='predicted_sales', color_continuous_scale='Greens')
st.plotly_chart(fig3, width='stretch')

st.markdown("### Prediction Results")
st.dataframe(filtered_df[['date', 'store_nbr', 'family',
                           'onpromotion', 'predicted_sales']].head(100))

result_csv = filtered_df[['date', 'store_nbr', 'family',
                           'onpromotion', 'predicted_sales']].to_csv(index=False)
st.download_button(
    label="Download Predictions as CSV",
    data=result_csv,
    file_name=f'predictions_{selected_year}.csv',
    mime='text/csv'
)

st.markdown("---")
st.markdown("### AI Business Insights")

if not api_key:
    st.warning("AI insights are temporarily unavailable.")
else:
    if st.button("Generate AI Insights"):
        with st.spinner("Generating insights..."):
            try:
                client = Groq(api_key=api_key)

                total_sales = filtered_df['predicted_sales'].sum()
                best_month = filtered_df.groupby('month')['predicted_sales'].sum().idxmax()

                prompt = f"""
You are a retail business analyst.
Based on these sales predictions for {selected_year}:
- Store Type filter: {selected_type}
- Total predicted sales: {total_sales:,.0f}
- Top performing store: Store {top_store}
- Top selling category: {top_cat}
- Best performing month: Month {best_month}
- Number of stores: {filtered_df['store_nbr'].nunique()}

Write exactly 3 business insights in this exact format:

INSIGHT 1 - STORE PERFORMANCE:
[Write insight and recommendation about store performance here]

INSIGHT 2 - PRODUCT STRATEGY:
[Write insight and recommendation about product category here]

INSIGHT 3 - TIMING STRATEGY:
[Write insight and recommendation about best time to sell here]

Be specific and actionable for each insight.
"""
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )

                raw_text = response.choices[0].message.content
                st.markdown("---")

                if "INSIGHT 1" in raw_text and "INSIGHT 2" in raw_text and "INSIGHT 3" in raw_text:
                    parts = raw_text.split("INSIGHT ")
                    parts = [p for p in parts if p.strip()]

                    icons = ["🏪", "📦", "📅"]
                    headings = [
                        "Store Performance",
                        "Product Strategy",
                        "Timing Strategy"
                    ]

                    for i, part in enumerate(parts[:3]):
                        lines = part.strip().split("\n")
                        content = "\n".join(lines[1:]).strip()
                        st.markdown(f"#### {icons[i]} Insight {i+1} — {headings[i]}")
                        st.info(content)
                        st.markdown("")
                else:
                    st.markdown("#### 🏪 Insight 1 — Store Performance")
                    st.markdown("#### 📦 Insight 2 — Product Strategy")
                    st.markdown("#### 📅 Insight 3 — Timing Strategy")
                    st.info(raw_text)

            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("Built by Dhanushya | ML Internship @ Future Interns")