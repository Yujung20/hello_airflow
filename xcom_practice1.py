from asyncio import tasks
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum

local_tz = pendulum.timezone("America/New_York")


def task_1(**kwargs):
    ti = kwargs["ti"]
    ti.xcom_push(key="my_data", value="Hello form task 1")


def task_2(**kwargs):
    ti = kwargs["ti"]
    value = ti.xcom_pull(task_ids="task_1", key="my_data")
    print(f"Received value : {value}")


with DAG(
    dag_id="xcom_practice1",
    start_date=datetime(2025, 10, 14, tzinfo=local_tz),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task_1_op = PythonOperator(
        task_id="task_1", python_callable=task_1, provide_context=True
    )
    task_2_op = PythonOperator(
        task_id="task_2", python_callable=task_2, provide_context=True
    )

    task_1_op >> task_2_op
