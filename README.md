# 📈 Sales & Demand Forecasting for Businesses

![Python](https://img.shields.io/badge/Python-3.14-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![Gemini](https://img.shields.io/badge/Gemini-AI-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

## 🔗 Live Demo
🚀 Coming soon — Streamlit deployment

---

## 📌 About This Project
I built a Sales & Demand Forecasting system using 
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
trained an XGBoost model, and built a complete 
forecasting pipeline.

On top of the ML model, I integrated Google Gemini 
API to automatically generate plain-English business 
insights from the predictions — so any store manager 
can understand the results without needing a data 
science background.

---

## 🔍 What I Did Step by Step
- Loaded and cleaned 3 million rows of retail sales data
- Merged store information to enrich the dataset
- Engineered 12 features including day of week, 
  month, quarter, weekend flag, store type
- Trained XGBoost model on 2.4 million rows
- Evaluated model using RMSE and MAE
- Built 7 business visualizations
- Integrated Gemini AI to generate business insights
- Tested model on completely new store data

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

---

## 🤖 AI Integration
After the model generates predictions I send the 
results to Google Gemini API which produces 
business insights like:

> "Store 2 is significantly underperforming with 
> zero promotional items. Implement 5-7 targeted 
> promotions for next month. Store 1 with 10 
> promotional items is the top performer at 
> 2321 units."

This makes the project useful for real business 
decision making — not just a data science exercise.

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
| Pandas & NumPy | Data cleaning and processing |
| XGBoost | Sales forecasting model |
| Scikit-learn | Model evaluation |
| Matplotlib & Seaborn | Data visualizations |
| Google Gemini API | AI business insights |
| Jupyter Notebook | Development environment |

---

## 📁 Dataset
I used the Store Sales Time Series Forecasting 
dataset from Kaggle:

[Download here](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)

Download train.csv and stores.csv and place 
them in the project folder before running.

---
