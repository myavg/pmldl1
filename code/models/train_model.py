# code/models/train_model.py
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import joblib

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "winequality-red.csv"
MODEL_PATH = ROOT / "models" / "wine_model.pkl"

def main():
    df = pd.read_csv(DATA_PATH)
    feature_cols = [
        "fixed acidity","volatile acidity","citric acid","residual sugar",
        "chlorides","free sulfur dioxide","total sulfur dioxide","density",
        "pH","sulphates","alcohol"
    ]
    X = df[feature_cols]
    y = df["quality"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipe = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("lr", LinearRegression())
    ])
    pipe.fit(X_train, y_train)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": pipe, "features": feature_cols}, MODEL_PATH)
    print(f"Saved model to: {MODEL_PATH}")

if __name__ == "__main__":
    main()
