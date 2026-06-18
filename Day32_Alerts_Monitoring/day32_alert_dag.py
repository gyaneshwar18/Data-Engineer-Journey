from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

sys.path.append(
    '/home/gyaneshwar/Data-Engineer-Journey/Day32_Alerts_Monitoring/src'
)

from pipelines.alert_pipeline import failing_task


# ----------------------------------------
# Alert Callback Function
# ----------------------------------------
def failure_alert(context):
    print("🚨 ALERT: Pipeline Failed!")
    print(f"Task Failed: {context['task_instance'].task_id}")
    print(f"DAG: {context['task_instance'].dag_id}")


with DAG(
    dag_id='day32_alert_monitoring',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False
) as dag:

    alert_task = PythonOperator(
        task_id='failing_pipeline',
        python_callable=failing_task,
        on_failure_callback=failure_alert
    )
