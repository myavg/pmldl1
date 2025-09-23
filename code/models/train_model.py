from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import mlflow

ROOT = Path(__file__).resolve().parents[2]
TRAIN = ROOT / "data" / "processed" / "train.csv"
TEST = ROOT / "data" / "processed" / "test.csv"
MODEL_PATH = ROOT / "models" / "wine_model.pkl"
MLRUNS_DIR = ROOT / "mlruns"

FEATURES = [
    "fixed acidity","volatile acidity","citric acid","residual sugar",
    "chlorides","free sulfur dioxide","total sulfur dioxide","density",
    "pH","sulphates","alcohol"
]
TARGET = "quality"

def main():
    train_df = pd.read_csv(TRAIN)
    test_df = pd.read_csv(TEST)

    X_train = train_df[FEATURES].copy()
    y_train = train_df[TARGET].copy()
    X_test = test_df[FEATURES].copy()
    y_test = test_df[TARGET].copy()

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("lr", LinearRegression())
    ])

    mlflow.set_tracking_uri(f"file:{MLRUNS_DIR.as_posix()}")
    mlflow.set_experiment("wine-quality")

    with mlflow.start_run(run_name="linreg-standard"):
        pipe.fit(X_train, y_train)

        y_pred = pipe.predict(X_test)
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        r2 = float(r2_score(y_test, y_pred))

        mlflow.log_metrics({"rmse": rmse, "r2": r2})
        mlflow.log_params({"model": "LinearRegression", "scaler": "StandardScaler"})

        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"model": pipe, "features": FEATURES}, MODEL_PATH)
        mlflow.log_artifact(MODEL_PATH, artifact_path="model")

        print(f"[Stage 2] RMSE={rmse:.4f}  R2={r2:.4f}")
        print(f"[Stage 2] Saved model to: {MODEL_PATH}")

if __name__ == "__main__":
    main()
