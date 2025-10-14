from asyncio import tasks
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum
import pandas as pd

local_tz = pendulum.timezone("America/New_York")


def save_to_csv(**kwargs):
    df = pd.DataFrame({"height": [177, 185, 162], "width": [200, 500, 100]})
    df.to_csv("/shared_path/output.csv", index=False)


def read_from_csv(**kwargs):
    df = pd.read_csv("/shared_path/output.csv")
    print(df)


with DAG(
    dag_id="xcom_practice2",
    start_date=datetime(2025, 10, 14, tzinfo=local_tz),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    save_task = PythonOperator(task_id="save_task", python_callable=save_to_csv)
    read_task = PythonOperator(task_id="read_task", python_callable=read_from_csv)

    save_task >> read_task
