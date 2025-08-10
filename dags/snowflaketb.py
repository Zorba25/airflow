# dags/count_snowflake_tables_airbnb_dev.py
from __future__ import annotations
from datetime import datetime
from airflow import DAG
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import PythonOperator

CONN_ID = "snowflake"

def log_table_count():
    hook = SnowflakeHook(snowflake_conn_id=CONN_ID)
    sql = """
        SELECT COUNT(*) AS table_count
        FROM AIRBNB.INFORMATION_SCHEMA.TABLES
        WHERE table_schema = 'DEV';
    """
    result = hook.get_first(sql)  # returns tuple, e.g. (3,)
    count = result[0]
    print(f"Number of tables in AIRBNB.DEV: {count}")

with DAG(
    dag_id="count_snowflake_tables_airbnb_dev",
    start_date=datetime(2025, 8, 10),
    schedule_interval=None,
    catchup=False,
    tags=["snowflake", "airbnb"],
) as dag:

    count_tables = PythonOperator(
        task_id="count_tables",
        python_callable=log_table_count,
    )

    count_tables
