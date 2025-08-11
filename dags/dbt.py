from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Paths based on your mounts in docker-compose
DBT_PROJECT_DIR = "/opt/airflow/dbtlearn"
DBT_PROFILES_DIR = "/opt/airflow/.dbt"

with DAG(
    dag_id="dbt_run_only_pipeline",
    schedule_interval="@daily",
    start_date=datetime(2025, 8, 11),
    catchup=False,
    tags=["dbt", "bash", "snowflake"],
) as dag:

    dbt_run = BashOperator(
    task_id="dbt_run",
    bash_command=f"""
        echo "📦 Installing dbt dependencies..."
        cd {DBT_PROJECT_DIR}
        export DBT_PROFILES_DIR={DBT_PROFILES_DIR}
        dbt deps  # Install package dependencies first
        
        echo "🚀 Running dbt models..."
        dbt run --target dev
        echo "✅ dbt run completed"
    """,
)
