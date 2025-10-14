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


# ✅ 1️⃣ Feature Engineering
def feature_engineering(**kwargs):
    ti = kwargs["ti"]

    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    # DataFrame으로 변환해서 로깅하기 좋게
    df_train = pd.DataFrame(X_train, columns=iris.feature_names)
    df_test = pd.DataFrame(X_test, columns=iris.feature_names)

    # XCom으로 데이터 전달
    ti.xcom_push(key="X_train", value=df_train.to_json())
    ti.xcom_push(key="X_test", value=df_test.to_json())
    ti.xcom_push(key="y_train", value=y_train.tolist())
    ti.xcom_push(key="y_test", value=y_test.tolist())

    print("✅ Feature engineering 완료 및 데이터 XCom 전달")


# ✅ 2️⃣ Model Training
def train_model(model_name, **kwargs):
    ti = kwargs["ti"]

    # XCom에서 데이터 불러오기
    import json

    X_train = pd.read_json(ti.xcom_pull(key="X_train", task_ids="feature_engineering"))
    X_test = pd.read_json(ti.xcom_pull(key="X_test", task_ids="feature_engineering"))
    y_train = ti.xcom_pull(key="y_train", task_ids="feature_engineering")
    y_test = ti.xcom_pull(key="y_test", task_ids="feature_engineering")

    # 모델 선택
    if model_name == "RandomForest":
        model = RandomForestClassifier(random_state=42)
    elif model_name == "GradientBoosting":
        model = GradientBoostingClassifier(random_state=42)
    else:
        raise ValueError("지원하지 않는 모델입니다.")

    # 학습 및 평가
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # 결과를 XCom으로 전달
    ti.xcom_push(key=f"{model_name}_accuracy", value=acc)
    print(f"✅ {model_name} 학습 완료 — 정확도: {acc:.4f}")


# ✅ 3️⃣ Model Selection
def select_best_model(**kwargs):
    ti = kwargs["ti"]

    rf_acc = ti.xcom_pull(key="RandomForest_accuracy", task_ids="train_rf")
    gb_acc = ti.xcom_pull(key="GradientBoosting_accuracy", task_ids="train_gb")

    print(f"📊 RandomForest 정확도: {rf_acc:.4f}")
    print(f"📊 GradientBoosting 정확도: {gb_acc:.4f}")

    if rf_acc > gb_acc:
        best_model = "RandomForest"
        best_acc = rf_acc
    else:
        best_model = "GradientBoosting"
        best_acc = gb_acc

    print(f"🏆 최적 모델: {best_model} (정확도 {best_acc:.4f})")
    ti.xcom_push(key="best_model", value=best_model)


# ✅ 4️⃣ Task 정의
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
