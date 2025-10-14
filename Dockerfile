FROM python:3.9-slim

ENV AIRFLOW_HOME=/usr/local/airflow

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    python3-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

RUN pip install "apache-airflow==2.9.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.9.txt"

RUN mkdir -p $AIRFLOW_HOME

WORKDIR $AIRFLOW_HOME

RUN airflow db init

RUN apt-get update && apt-get install -y supervisor

COPY supervisord.conf /etc/supervisor/supervisord.conf 

COPY my_dag.py $AIRFLOW_HOME/dags/

EXPOSE 8080

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]