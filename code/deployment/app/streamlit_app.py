# code/deployment/app/streamlit_app.py
import os
import requests
import streamlit as st

st.set_page_config(page_title="Wine Quality Predictor (0-10)", page_icon="🍷", layout="centered")

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("🍷 Wine Quality Predictor (red)")

with st.expander("Wine parameters"):
    c1, c2 = st.columns(2)
    fixed_acidity = c1.number_input("fixed acidity", value=7.4, format="%.3f")
    volatile_acidity = c2.number_input("volatile acidity", value=0.700, format="%.3f")
    citric_acid = c1.number_input("citric acid", value=0.000, format="%.3f")
    residual_sugar = c2.number_input("residual sugar", value=1.900, format="%.3f")
    chlorides = c1.number_input("chlorides", value=0.076, format="%.3f")
    free_sulfur_dioxide = c2.number_input("free sulfur dioxide", value=11.0, format="%.1f")
    total_sulfur_dioxide = c1.number_input("total sulfur dioxide", value=34.0, format="%.1f")
    density = c2.number_input("density", value=0.9978, format="%.4f")
    pH = c1.number_input("pH", value=3.51, format="%.2f")
    sulphates = c2.number_input("sulphates", value=0.56, format="%.2f")
    alcohol = c1.number_input("alcohol", value=9.4, format="%.1f")

if st.button("Make prediction"):
    payload = {
        "fixed acidity": fixed_acidity,
        "volatile acidity": volatile_acidity,
        "citric acid": citric_acid,
        "residual sugar": residual_sugar,
        "chlorides": chlorides,
        "free sulfur dioxide": free_sulfur_dioxide,
        "total sulfur dioxide": total_sulfur_dioxide,
        "density": density,
        "pH": pH,
        "sulphates": sulphates,
        "alcohol": alcohol
    }
    r = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
    r.raise_for_status()
    pred = r.json()
    st.success(f"Quality: **{pred['quality_pred']}** (Score: {pred['quality_pred_raw']:.3f})")

st.divider()