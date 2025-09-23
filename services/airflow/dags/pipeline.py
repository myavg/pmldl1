from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from pathlib import Path
import subprocess, sys, os

REPO = Path(os.getenv("REPO_DIR", "/repo")).resolve()

def _run(pyfile: Path):
    subprocess.check_call([sys.executable, str(pyfile)], cwd=str(REPO))

def _stage1():
    _run(REPO / "code" / "datasets" / "make_dataset.py")

def _stage2():
    _run(REPO / "code" / "models" / "train_model.py")

def _stage3():
    _run(REPO / "code" / "deployment" / "deploy.py")

default_args = {"owner": "airflow", "retries": 0, "retry_delay": timedelta(minutes=1)}

with DAG(
    dag_id="wine_pipeline_every_5_min",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="*/5 * * * *",
    catchup=False,
    tags=["wine", "ml", "demo"],
) as dag:
    stage1 = PythonOperator(task_id="stage1_make_dataset", python_callable=_stage1)
    stage2 = PythonOperator(task_id="stage2_train_and_log", python_callable=_stage2)
    stage3 = PythonOperator(task_id="stage3_build_and_run", python_callable=_stage3)
    stage1 >> stage2 >> stage3
