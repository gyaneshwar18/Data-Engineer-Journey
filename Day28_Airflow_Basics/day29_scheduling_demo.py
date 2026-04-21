from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

# connect your pipeline
sys.path.append('/home/gyaneshwar/Data-Engineer-Journey/Day28_Airflow_Basics/src')

from pipelines.etl_pipeline import run_pipeline


def run_etl():
    print("Running Scheduled ETL...")
    run_pipeline()


# -------------------------------
# 1️⃣ DAILY PIPELINE
# -------------------------------
with DAG(
    dag_id='day29_daily_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False
) as daily_dag:

    daily_task = PythonOperator(
        task_id='run_daily',
        python_callable=run_etl
    )


# -------------------------------
# 2️⃣ EVERY 5 MINUTES
# -------------------------------
with DAG(
    dag_id='day29_every_5_min',
    start_date=datetime(2024, 1, 1),
    schedule='*/5 * * * *',
    catchup=False
) as fast_dag:

    fast_task = PythonOperator(
        task_id='run_fast',
        python_callable=run_etl
    )


# -------------------------------
# 3️⃣ CUSTOM CRON (2 AM)
# -------------------------------
with DAG(
    dag_id='day29_custom_cron',
    start_date=datetime(2024, 1, 1),
    schedule='0 2 * * *',
    catchup=False
) as cron_dag:

    cron_task = PythonOperator(
        task_id='run_cron',
        python_callable=run_etl
    )
