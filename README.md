# Wine Quality ML Pipeline — Data → Model → Deployment
cd ~/services/airflow

docker compose up -d

After building, go to http://localhost:8501/ for app.

And http://localhost:8080/ for airflow (name:admin password: admin).

Short, working example of a 3-stage ML pipeline scheduled every 5 minutes with Airflow:

Data engineering → load, clean, split → data/processed/{train,test}.csv

Model engineering → features, train, evaluate (RMSE, R²), save model → models/wine_model.pkl, logs in mlruns/

Deployment → build & run FastAPI (model API) and Streamlit (UI) in separate Docker containers

What happens in each stage:

Stage 1 — Data engineering (code/datasets/make_dataset.py)

Reads data/winequality-red.csv

Cleans data (median imputation, IQR outlier removal)

Stratified split → writes data/processed/train.csv and data/processed/test.csv

Stage 2 — Model engineering (code/models/train_model.py)

Builds pipeline: StandardScaler → LinearRegression

Trains on train.csv, evaluates on test.csv

Logs metrics to MLflow

Saves packed model (pipeline + feature list) to models/wine_model.pkl

Stage 3 — Deployment (code/deployment/deploy.py)

Uses Docker to build images:

api (FastAPI)

app (Streamlit)

Recreates containers wine_api and wine_app in one Docker network

Orchestration — Airflow (services/airflow/dags/pipeline.py)

Three PythonOperator tasks: stage1 → stage2 → stage3

Schedule: */5 * * * * (runs every five minutes)

Runs scripts as separate processes