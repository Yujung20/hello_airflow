from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import pendulum  # Pendulum is the recommended library for timezone management in Airflow
import pandas as pd

local_tz = pendulum.timezone("Asia/Seoul")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 26, tzinfo=local_tz),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "model_training_and_selection",
    default_args=default_args,
    description="Using DAG for model training and selection",
    schedule_interval=timedelta(days=1),
)


def feature_engineering(kwargs):
    pass


def train_model(model_name, kwargs):
    pass


def select_best_model(**kwargs):
    pass


with dag:
    t1 = PythonOperator(
        task_id="feature_engineering",
        python_callable=feature_engineering,
    )

    t2 = PythonOperator(
        task_id="train_rf",
        python_callable=train_model,
        op_kwargs={"model_name": "RandomForest"},
        provide_context=True,
    )

    t3 = PythonOperator(
        task_id="train_gb",
        python_callable=train_model,
        op_kwargs={"model_name": "GradientBoosting"},
        provide_context=True,
    )

    t4 = PythonOperator(
        task_id="select_best_model",
        python_callable=select_best_model,
        provide_context=True,
    )

    t1 >> [t2, t3] >> t4
