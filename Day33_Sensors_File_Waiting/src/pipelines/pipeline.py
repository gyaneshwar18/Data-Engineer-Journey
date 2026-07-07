from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

sys.path.append(
    "/home/gyaneshwar/Data-Engineer-Journey/Day33_Sensors_File_Waiting/src"
)

from pipelines.file_pipeline import process_file

with DAG(
    dag_id="day33_file_sensor",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath="/tmp/input_file.txt",
        poke_interval=10,
        timeout=60
    )

    process_task = PythonOperator(
        task_id="process_file",
        python_callable=process_file
    )

    wait_for_file >> process_task