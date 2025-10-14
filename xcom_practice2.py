from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum
import pandas as pd
import os

local_tz = pendulum.timezone("America/New_York")


def save_to_csv(**kwargs):
    output_dir = "/usr/local/airflow/dags/shared_path"
    os.makedirs(output_dir, exist_ok=True)  # 폴더 없으면 자동 생성

    df = pd.DataFrame({"height": [177, 185, 162], "width": [200, 500, 100]})
    output_path = f"{output_dir}/output.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"✅ CSV 저장 완료: {output_path}")


def read_from_csv(**kwargs):
    file_path = "/usr/local/airflow/dags/shared_path/output.csv"
    df = pd.read_csv(file_path, encoding="utf-8")
    print("✅ CSV 내용:\n", df)


with DAG(
    dag_id="xcom_practice2",
    start_date=datetime(2025, 10, 14, tzinfo=local_tz),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    save_task = PythonOperator(
        task_id="save_task",
        python_callable=save_to_csv,
        provide_context=True,
    )

    read_task = PythonOperator(
        task_id="read_task",
        python_callable=read_from_csv,
        provide_context=True,
    )

    save_task >> read_task
