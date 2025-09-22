# code/deployment/app/Dockerfile
FROM python:3.11

WORKDIR /app

COPY code/deployment/app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY code/deployment/app /app

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
