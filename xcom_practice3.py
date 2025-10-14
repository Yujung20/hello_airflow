from asyncio import tasks
from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum
import pandas as pd

local_tz = pendulum.timezone("America/New_York")


with DAG(
    dag_id="xcom_practice3",
    start_date=datetime(2025, 10, 14, tzinfo=local_tz),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    insert_task = MySqlOperator(task_id="insert_task")
    select_task = MySqlOperator(task_id="select_task")

    insert_task >> select_task
