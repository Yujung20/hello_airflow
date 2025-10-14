from asyncio import tasks
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum

local_tz = pendulum.timezone("Asia/Seoul")

default_args = {
    "owner": "Yujung20",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1, tzinfo=local_tz),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "Hello_Airflow_PythonOperator",
    default_args=default_args,
    description="my first airflow practice",
    schedule_interval=timedelta(days=1),
)

input_words = "python very easy, airflow very easy."


def review_word(word):
    print(word)


previous_task = None
for i, word in enumerate(input_words.split()):
    task = PythonOperator(
        task_id=f"word_{i}",
        python_callable=review_word,
        op_kwargs={"word": word},
        dag=dag,
    )

    if previous_task:
        previous_task >> task
