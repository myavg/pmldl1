FROM python:3.11 AS base
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# ---- API ----
FROM base AS api
COPY code/deployment/api /app
COPY models /app/models
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# ---- Streamlit ----
FROM base AS app
ENV API_URL=http://api:8000
COPY code/deployment/app /app
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
