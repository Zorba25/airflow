from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Simple Python function
def hello_world():
    print("Hello from Airflow!")

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Create the DAG
with DAG(
    dag_id='hello_world_dag',
    default_args=default_args,
    description='A simple test DAG',
    schedule_interval=None,  # Run manually
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id='print_hello',
        python_callable=hello_world
    )

    task1
