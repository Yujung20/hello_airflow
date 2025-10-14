from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import pendulum
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
    catchup=False,
)


def feature_engineering(**kwargs):
    # load the iris data
    iris = load_iris()
    x = pd.DataFrame(iris["data"], columns=iris["feature_names"])
    y = pd.Series(iris["target"], name="target")

    # Data 분할(x_train, x_test, y_train, y_test)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    # XCom을 이용해 데이터 저장
    ti = kwargs["ti"]
    ti.xcom_push(key="x_train", value=x_train.to_json())
    ti.xcom_push(key="x_test", value=x_test.to_json())
    ti.xcom_push(key="y_train", value=y_train.to_json(orient="records"))
    ti.xcom_push(key="y_test", value=y_test.to_json(orient="records"))


def train_model(model_name, **kwargs):
    # XCom에서 데이터 불러오기
    ti = kwargs["ti"]
    x_train = pd.read_json(ti.xcom_pull(key="x_train", task_ids="feature_engineering"))
    x_test = pd.read_json(ti.xcom_pull(key="x_test", task_ids="feature_engineering"))
    y_train = pd.Series(
        ti.xcom_pull(key="y_train", task_ids="feature_engineering"), typ="series"
    )
    y_test = pd.Series(
        ti.xcom_pull(key="y_test", task_ids="feature_engineering"), typ="series"
    )
    # 모델 학습
    if model_name == "RandomForest":
        model = RandomForestClassifier(random_state=42)
    elif model_name == "GradientBoosting":
        model = GradientBoostingClassifier(random_state=42)
    else:
        raise ValueError("Unsupported model name")

    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    # 모델 평가(accuracy)
    acc = accuracy_score(y_test, y_pred)

    # 평과 결과를 XCom에 저장
    ti.xcom_push(key=f"acc_{model_name}", value=acc)


def select_best_model(**kwargs):

    # XCom에서 두 모델의 평가 결과 불러오기
    ti = kwargs["ti"]

    rf_acc = ti.xcom_pull(key="acc_RandomForest", task_ids="train_rf")
    gb_acc = ti.xcom_pull(key="acc_GradientBoosting", task_ids="train_gb")

    # 더 좋은 모델이 무엇인지? 출력
    best_model = "RandomForest" if rf_acc < gb_acc else "GradientBoosting"
    print(f"the best models is {best_model} with accuracy {max(rf_acc, gb_acc)}")


with dag:
    t1 = PythonOperator(
        task_id="feature_engineering",
        python_callable=feature_engineering,
        provide_context=True,
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
