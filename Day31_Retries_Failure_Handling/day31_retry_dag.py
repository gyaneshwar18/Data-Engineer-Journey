from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append(
    '/home/gyaneshwar/Data-Engineer-Journey/Day31_Retries_Failure_Handling/src'
)

from src.pipelines.retry_pipeline import unstable_task


default_args = {
    'owner': 'gyan',
    'retries': 2,
    'retry_delay': timedelta(seconds=10)
}


with DAG(
    dag_id='day31_retry_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
    default_args=default_args
) as dag:

    retry_task = PythonOperator(
        task_id='unstable_task',
        python_callable=unstable_task
    )
