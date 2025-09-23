from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "winequality-red.csv"
OUT_DIR = ROOT / "data" / "processed"
TRAIN = OUT_DIR / "train.csv"
TEST = OUT_DIR / "test.csv"
RANDOM_STATE = 42
TEST_SIZE = 0.2

FEATURES = [
    "fixed acidity","volatile acidity","citric acid","residual sugar",
    "chlorides","free sulfur dioxide","total sulfur dioxide","density",
    "pH","sulphates","alcohol"
]
TARGET = "quality"

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in FEATURES + [TARGET]:
        if df[c].isna().any():
            df[c] = df[c].fillna(df[c].median())

    mask = pd.Series(True, index=df.index)
    for c in FEATURES:
        q1, q3 = df[c].quantile([0.25, 0.75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask &= df[c].between(low, high)
    return df[mask].reset_index(drop=True)

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW)
    df = clean_df(df)

    from sklearn.model_selection import train_test_split
    train_df, test_df = train_test_split(
        df, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=df[TARGET]
    )
    train_df.to_csv(TRAIN, index=False)
    test_df.to_csv(TEST, index=False)
    print(f"[Stage 1] Saved: {TRAIN} ({len(train_df)} rows), {TEST} ({len(test_df)} rows)")

if __name__ == "__main__":
    main()
