# HELLO_AIRFLOW

Docker 기반 Apache Airflow 실습 프로젝트<br>
**(ENG)Docker-based Apache Airflow practice project**

---

## Skills

- Python
- Apache Airflow
- Docker
- Supervisor

---

## Project Summary

Docker 환경에서 Apache Airflow를 실행하고,<br>
DAG 기반 workflow 및 XCom 기능을 실습한 프로젝트입니다.<br>

task dependency와 task 간 데이터 전달 구조를 학습했습니다.

**Eng ver.** 

This project was created to practice running Apache Airflow in a Docker environment and to understand DAG-based workflows and XCom features.

It includes task dependency configuration and inter-task data communication using XCom.


---

## Purpose

- Airflow 기본 구조 이해
- Docker 기반 실행 환경 구성 경험
- DAG 기반 workflow orchestration 학습
- XCom을 활용한 task 간 데이터 전달 실습

**Eng ver.** 

- Understand the basic structure of Apache Airflow
- Gain experience with Docker-based environment setup
- Learn DAG-based workflow orchestration
- Practice inter-task communication using XCom

---

## Why I Built This

데이터 파이프라인 자동화와 workflow orchestration 구조에 관심이 생기면서,<br>
Apache Airflow가 실제로 어떤 방식으로 task를 관리하는지 직접 경험해보기 위해 진행했습니다.<br>

또한 Docker 기반 환경 구성을 통해
컨테이너 실행 환경과 서비스 관리 구조를 함께 학습하고자 했습니다.

**Eng ver.** 

As I became interested in data pipeline automation and workflow orchestration, I wanted to explore how Apache Airflow manages and executes tasks in practice.

I also wanted to learn how containerized environments work by building and running Airflow using Docker.


---

## Project Structure

```text
HELLO_AIRFLOW/
├── Dockerfile
├── hello_airflow_dag.py
├── ml_airflow_dag.py
├── supervisord.conf
├── test.ipynb
├── xcom_practice1.py
├── xcom_practice2.py
└── xcom_practice3.py
```

---

## Main Features

### Airflow DAG 구성

- PythonOperator 기반 task 작성
- task dependency 설정 실습

&nbsp;&nbsp; **Eng ver.** 

- Created tasks using PythonOperator
- Practiced task dependency configuration

### XCom 실습

- task 간 데이터 전달 구조 실습
- `xcom_push`, `xcom_pull` 사용

&nbsp;&nbsp;**Eng ver.** 

- Practiced inter-task data communication
- Used `xcom_push` and `xcom_pull`

### Docker 환경 구성

- Docker 기반 Airflow 실행 환경 구성
- 컨테이너 환경에서 workflow 실행 실습

&nbsp;&nbsp;**Eng ver.** 

- Built an Airflow execution environment using Docker
- Practiced running workflows in a containerized environment

---

## How to Run

```bash
docker build -t hello_airflow .
docker run hello_airflow
```

---

## What I Learned

- Docker 기반 실행 환경 구성 방식 이해
- Airflow DAG 구조 및 workflow orchestration 개념 학습
- task dependency 설정 방식 경험
- XCom을 활용한 task 간 데이터 전달 구조 이해

**Eng ver.** 

- Understanding Docker-based execution environments
- Learning DAG-based workflow orchestration concepts
- Understanding task dependency configuration
- Practicing inter-task communication using XCom

---

