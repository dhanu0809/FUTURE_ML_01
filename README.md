# 📈 Sales & Demand Forecasting for Businesses

![Python](https://img.shields.io/badge/Python-3.14-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

## 🔗 Live Demo
🚀 [Click here to try the app](https://your-streamlit-link-here)

---

## 📌 About This Project
I built a Sales and Demand Forecasting system using
real retail store data from 54 stores across Ecuador
covering 2013 to 2017. The goal was to predict future
sales and generate actionable business insights for
store managers.

This is Task 1 of my Machine Learning Internship
at Future Interns.

---

## 💡 What I Built
I started with raw sales data containing 3 million
rows across 33 product categories and 54 stores.
I cleaned the data, engineered time-based features,
trained an XGBoost model using a chronological
train-test split to prevent data leakage, and
built a complete forecasting pipeline.

On top of the ML model, I integrated Groq LLaMA
3.3 70B API to automatically generate structured
business insights from predictions — so any store
manager can understand results without needing a
data science background.

I also built a fully interactive Streamlit web app
where anyone can upload sales data, view charts,
and get AI insights instantly.

---

## 🔍 What I Did Step by Step
- Loaded and cleaned 3 million rows of retail
  sales data
- Merged store information to enrich the dataset
- Engineered 12 time-based features including
  day of week, month, quarter, weekend flag,
  store type
- Applied chronological train-test split to
  prevent data leakage in time-series forecasting
- Trained XGBoost model on 2.4 million rows
- Evaluated model using RMSE and MAE
- Built 7 business visualizations
- Integrated Groq LLaMA 3.3 70B to generate
  structured AI insights from predictions
- Tested model on completely new store data
- Built and deployed a Streamlit web app

---

## 📊 Model Performance
| Metric | Value |
|--------|-------|
| RMSE | 415.15 |
| MAE | 140.87 |
| Training rows | 2.4 million |
| Test rows | 600k |
| Features | 12 |
| Top feature | Promotions (30%) |
| Split type | Chronological |

---

## 🔄 Model Maintenance Note
This model uses chronological train-test split
(2013-2016 training, 2017 testing) to prevent
data leakage — a critical requirement for
time-series forecasting.

In production, scheduled monthly retraining
would handle model drift as customer behavior,
pricing, and promotions change over time.

---

## 🤖 AI Integration
After the model generates predictions I send the
results to Groq LLaMA 3.3 70B API which produces
3 structured business insights:

**🏪 Insight 1 — Store Performance**
Which store is performing best and how to
replicate its strategies across other stores.

**📦 Insight 2 — Product Strategy**
Which product category drives the most revenue
and how to optimize stock and promotions.

**📅 Insight 3 — Timing Strategy**
Which month has peak sales and how to plan
campaigns to maximize that period.

> Example output: Store Type D is the top
> performer. GROCERY I is the highest revenue
> category. July is peak month — plan promotions
> and increase stock accordingly.

---

## 🌐 Streamlit App Features
I built an interactive web app where anyone can:
- Use existing forecast data directly
- Upload any new sales CSV for fresh predictions
- Filter results by year and store type
- View 3 interactive Plotly charts
- Download predictions as CSV
- Download sample template CSV
- Generate AI business insights with one click

---

## 📉 Visualizations I Created
- Total Sales Trend 2013 to 2017
- Top 10 Product Categories by Revenue
- Sales Performance by Store Type
- XGBoost Feature Importance
- Actual vs Predicted Sales Comparison
- Monthly Forecasted Sales
- New Store Predictions

---

## 🛠️ Tech Stack
| Tool | How I Used It |
|------|--------------|
| Python 3.14 | Core development |
| Pandas and NumPy | Data cleaning and processing |
| XGBoost | Sales forecasting model |
| Scikit-learn | Model evaluation |
| Matplotlib and Seaborn | Data visualizations |
| Plotly | Interactive charts in Streamlit |
| Groq LLaMA 3.3 70B | AI business insights |
| Streamlit | Web app and deployment |
| Jupyter Notebook | Development environment |

---

## 📁 Dataset
I used the Store Sales Time Series Forecasting
dataset from Kaggle:

[Download here](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)

Download train.csv and stores.csv and place
them in the project folder before running.

---

## 🏢 Internship Details
**Organization:** Future Interns
**Track:** Machine Learning
**Task:** 1 — Sales and Demand Forecasting
**GitHub:** github.com/dhanu0809