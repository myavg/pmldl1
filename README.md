# Wine Quality ML Pipeline — Data → Model → Deployment

## 🚀 Quick Start

### Run via Airflow
```bash
cd services/airflow
docker compose up -d
```
Airflow UI → http://localhost:8080 (admin/admin)

Streamlit App UI → http://localhost:8501/

P.S. Please, wait couple of minutes if pages not loading.

---
# 📸 Screenshots

✅ Airflow DAG:

![Airflow success](pipeline_example.jpg)

🎛️ Streamlit UI:

![Streamlit UI](app_ui.jpg)

---

## ⚙️ Stages

### Stage 1 — Data Engineering
- Loads raw dataset (`data/winequality-red.csv`)
- Cleans missing values & removes outliers (IQR)
- Splits into train/test with stratification
- Outputs → `data/processed/train.csv` & `test.csv`

### Stage 2 — Model Engineering
- Pipeline: `StandardScaler` → `LinearRegression`
- Trains on train data, evaluates on test data
- Logs metrics (RMSE, R²) into **MLflow** (`mlruns/`)
- Saves model to `models/wine_model.pkl`

### Stage 3 — Deployment
- Builds Docker images from single `Dockerfile`:
  - `wine_api` (FastAPI) → port `8000`
  - `wine_app` (Streamlit) → port `8501`
- Runs containers in shared network

### Orchestration — Airflow
- DAG: `wine_pipeline_every_5_min`
- Three tasks: `stage1_make_dataset → stage2_train_and_log → stage3_build_and_run`
- Schedule: `*/5 * * * *`

---
