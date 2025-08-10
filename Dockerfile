FROM apache/airflow:2.6.1
RUN pip install --no-cache-dir \
    snowflake-connector-python \
    apache-airflow-providers-snowflake
