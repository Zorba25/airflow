from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

REPO_URL = "https://github.com/Zorba25/dblearn.git"
CLONE_PATH = "/opt/airflow/dags/dbt/dblearn"

with DAG(
    dag_id='simple_git_and_dbt',
    schedule_interval='@daily',
    start_date=datetime(2025, 8, 11),
    catchup=False,
) as dag:

    clone_repo = BashOperator(
        task_id='git_clone',
        bash_command=f"""
            mkdir -p {CLONE_PATH} && \
            rm -rf {CLONE_PATH}/* && \
            git clone {REPO_URL} {CLONE_PATH}
        """,
    )

    run_dbt = BashOperator(
        task_id='dbt_run',
        bash_command=f"""
            cd {CLONE_PATH} && \
            pip install --quiet --upgrade pip setuptools wheel && \
            pip install --quiet dbt-snowflake==1.8.0 && \
            export DBT_PROFILES_DIR=/opt/airflow/.dbt && \
            dbt run --profiles-dir /opt/airflow/.dbt
        """,
    )

    clone_repo >> run_dbt
