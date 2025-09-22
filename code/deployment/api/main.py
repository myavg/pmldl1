from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from pathlib import Path
import os
import numpy as np
import joblib

app = FastAPI(title="Wine Quality API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = Path(os.getenv("MODEL_PATH", str(APP_DIR / "models" / "wine_model.pkl")))

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found at {MODEL_PATH}."
    )

artifact = joblib.load(MODEL_PATH)
model = artifact["model"]
FEATURES: List[str] = artifact["features"]

class WineRequest(BaseModel):
    fixed_acidity: float = Field(..., alias="fixed acidity")
    volatile_acidity: float = Field(..., alias="volatile acidity")
    citric_acid: float = Field(..., alias="citric acid")
    residual_sugar: float = Field(..., alias="residual sugar")
    chlorides: float
    free_sulfur_dioxide: float = Field(..., alias="free sulfur dioxide")
    total_sulfur_dioxide: float = Field(..., alias="total sulfur dioxide")
    density: float
    pH: float
    sulphates: float
    alcohol: float

    def to_row(self) -> List[float]:
        mapping = {
            "fixed acidity": self.fixed_acidity,
            "volatile acidity": self.volatile_acidity,
            "citric acid": self.citric_acid,
            "residual sugar": self.residual_sugar,
            "chlorides": self.chlorides,
            "free sulfur dioxide": self.free_sulfur_dioxide,
            "total sulfur dioxide": self.total_sulfur_dioxide,
            "density": self.density,
            "pH": self.pH,
            "sulphates": self.sulphates,
            "alcohol": self.alcohol,
        }
        return [mapping[f] for f in FEATURES]

class PredictionResponse(BaseModel):
    quality_pred: int
    quality_pred_raw: float

@app.post("/predict", response_model=PredictionResponse)
def predict(req: WineRequest):
    x = np.array([req.to_row()])
    raw = float(model.predict(x)[0])
    rounded = int(np.clip(round(raw), 0, 10))
    return {"quality_pred": rounded, "quality_pred_raw": raw}
