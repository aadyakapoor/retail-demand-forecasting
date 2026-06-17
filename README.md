# \# Retail Demand Forecasting System

# 

# End-to-end demand forecasting system built on Walmart's M5 dataset — predicts daily unit sales for retail SKUs 28+ days into the future, served via a live API and interactive dashboard.

# 

# 🔗 \*\*Live Dashboard:\*\* https://retail-demand-forecasting-mwahuymcg5jiv9nxukmq8t.streamlit.app

# 

# 🔗 \*\*Live API Docs:\*\* https://retail-demand-forecasting-sua5.onrender.com/docs

# 

# \---

# 

# \## Overview

# 

# Retailers need accurate demand forecasts to avoid stockouts and overstocking. This project builds a forecasting pipeline on real Walmart sales data (CA state, top 50 SKUs across 4 stores), benchmarks multiple modelling approaches, and deploys the best-performing model as a production-style REST API with a live dashboard.

# 

# \---

# 

# \## Architecture

# 

# ```text

# Raw M5 Data (sales, calendar, prices)

# &#x20;       ↓

# Feature Engineering (lags, rolling stats, calendar, events, price)

# &#x20;       ↓

# Model Training \& Benchmarking (LightGBM vs Prophet vs Ensemble)

# &#x20;       ↓

# MLflow (experiment tracking, model registry)

# &#x20;       ↓

# FastAPI (REST API serving forecasts)

# &#x20;       ↓

# Docker → Render (live deployment)

# &#x20;       ↓

# Streamlit Dashboard (interactive visualization)

# ```

# 

# \---

# 

# \## Results

# 

# | Model    | RMSE (Units Sold/Day) | Notes                                         |

# | -------- | --------------------- | --------------------------------------------- |

# | LightGBM | 7.43                  | Selected as production model                  |

# | Prophet  | 11.41                 | Underperformed on sparse, intermittent demand |

# | Ensemble | 7.40–7.71             | No meaningful improvement over LightGBM alone |

# 

# Validation used \*\*walk-forward splitting\*\* (train on past, test on future) rather than random splits, avoiding data leakage and reflecting real-world deployment conditions.

# 

# \---

# 

# \## Dataset

# 

# \* Walmart M5 Forecasting Dataset

# \* California state stores only

# \* Top 50 products by sales volume

# \* 4 stores per product

# \* Total forecasted series: \*\*200 SKU-store combinations\*\*

# 

# \---

# 

# \## Exploratory Data Analysis Highlights

# 

# \* Strong weekly seasonality observed across many products

# \* Significant variation in demand between stores

# \* Highly intermittent demand for several products (50%+ zero-sale days)

# \* SNAP benefit days showed approximately \*\*9.7% uplift\*\* in average sales

# \* Product-level demand distributions were highly skewed

# 

# \---

# 

# \## Features Engineered

# 

# \### Lag Features

# 

# \* Sales lag (7 days)

# \* Sales lag (14 days)

# \* Sales lag (28 days)

# 

# \### Rolling Statistics

# 

# \* Rolling mean (7 days)

# \* Rolling mean (28 days)

# \* Rolling standard deviation (7 days)

# \* Rolling standard deviation (28 days)

# 

# \### Calendar Features

# 

# \* Day of week

# \* Month

# \* Week of year

# \* Weekend indicator

# 

# \### Event Features

# 

# \* Sporting events

# \* Cultural events

# \* Religious events

# \* National events

# 

# \### Pricing Features

# 

# \* Current price

# \* Relative price

# \* Price change percentage

# 

# \### Other Features

# 

# \* SNAP benefit indicator

# \* Historical demand trends

# 

# \---

# 

# \## Model Benchmarking

# 

# \### LightGBM

# 

# \* Best overall performance

# \* Captured seasonality and demand patterns effectively

# \* Selected for production deployment

# 

# \### Prophet

# 

# \* Easy baseline model

# \* Struggled with sparse and intermittent demand

# \* Higher RMSE than LightGBM

# 

# \### Ensemble

# 

# \* Combined LightGBM and Prophet predictions

# \* Produced marginal changes

# \* Did not consistently outperform LightGBM

# 

# \---

# 

# \## Tech Stack

# 

# \* Python

# \* pandas

# \* NumPy

# \* LightGBM

# \* Prophet

# \* MLflow

# \* FastAPI

# \* Docker

# \* Render

# \* Streamlit

# \* Plotly

# 

# \---

# 

# \## Project Structure

# 

# ```text

# retail-demand-forecasting/

# │

# ├── data/

# │   ├── subset.csv

# │   ├── df\_features.csv

# │   └── latest\_per\_item.csv

# │

# ├── notebooks/

# │   ├── 01\_data\_loading.ipynb

# │   ├── 02\_eda.ipynb

# │   ├── 03\_feature\_engineering.ipynb

# │   ├── 04\_lightgbm\_model.ipynb

# │   ├── 05\_mlflow.ipynb

# │   └── 06\_prophet\_ensemble.ipynb

# │

# ├── src/

# │   ├── api/

# │   │   ├── main.py

# │   │   └── predictor.py

# │   │

# │   └── models/

# │       ├── lgbm\_best.pkl

# │       ├── feature\_cols.json

# │       └── ensemble\_config.json

# │

# ├── dashboard/

# │   └── app.py

# │

# ├── docker/

# │   └── Dockerfile

# │

# ├── assets/

# │   ├── dashboard.png

# │   ├── mlflow\_experiments.png

# │   ├── feature\_importance.png

# │   └── model\_comparison.png

# │

# ├── requirements.txt          # Streamlit dashboard dependencies

# ├── requirements-api.txt      # FastAPI/Docker dependencies

# └── README.md

# ```

# 

# \---

# 

# \## Running Locally

# 

# \### Clone Repository

# 

# ```bash

# git clone https://github.com/aadyakapoor/retail-demand-forecasting.git

# cd retail-demand-forecasting

# ```

# 

# \### Run API

# 

# ```bash

# pip install -r requirements-api.txt

# 

# cd src/api

# 

# uvicorn main:app --reload --port 8000

# ```

# 

# Open:

# 

# ```text

# http://localhost:8000/docs

# ```

# 

# \### Run Dashboard

# 

# ```bash

# pip install -r requirements.txt

# 

# streamlit run dashboard/app.py

# ```

# 

# \---

# 

# \## API Endpoints

# 

# \### Health Check

# 

# ```http

# GET /health

# ```

# 

# \### Available Items

# 

# ```http

# GET /items

# ```

# 

# Returns all available SKU-store combinations.

# 

# \### Forecast

# 

# ```http

# POST /forecast

# ```

# 

# Example request:

# 

# ```json

# {

# &#x20; "item\_id": "FOODS\_3\_362\_CA\_1\_evaluation",

# &#x20; "horizon": 28

# }

# ```

# 

# \---

# 

# \## Deployment

# 

# \### API

# 

# \* FastAPI

# \* Dockerized

# \* Hosted on Render

# 

# \### Dashboard

# 

# \* Streamlit

# \* Hosted on Streamlit Community Cloud

# 

# \---

# 

# \## Key Learnings

# 

# \* Walk-forward validation is essential for honest time-series evaluation

# \* Lag and rolling-window features were stronger predictors than calendar variables alone

# \* Intermittent demand is challenging for traditional regression models

# \* More models do not necessarily improve performance

# \* Production ML involves deployment, monitoring, experiment tracking, and user-facing applications in addition to model building

# 

# \---

# 

# \## Screenshots

# 

# \### Dashboard

# 

# !\[Dashboard](./assets/dashboard.png)

# 

# \### MLflow Experiments

# 

# !\[MLflow Experiments](./assets/mlflow\_experiments.png)

# 

# \### Feature Importance

# 

# !\[Feature Importance](./assets/feature\_importance.png)

# 

# \### Model Comparison

# 

# !\[Model Comparison](./assets/model\_comparison.png)

# 

# \---

# 

# \## Author

# 

# \*\*Aadya Kapoor\*\*

# 

# Computer Science Student

# 

# Built an end-to-end retail demand forecasting system using Walmart's M5 dataset, covering exploratory data analysis, feature engineering, model benchmarking, MLflow experiment tracking, FastAPI deployment, Dockerization, Render hosting, and Streamlit dashboard development.

