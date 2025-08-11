# Use a newer Airflow image for better Python & dependency compatibility
FROM apache/airflow:2.10.2-python3.10

# Switch to root to install system packages
USER root

# Install system dependencies FIRST (as root)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3-venv \
       rustc \
       cargo \
       git \
       curl \
       unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify git installation (as root)
RUN git --version && echo "✅ Git installed successfully"

# Switch back to airflow user for Python package installation
USER airflow

# Upgrade pip tooling before installing packages
RUN pip install --upgrade pip setuptools wheel

# Add cache bust to force rebuild of Python packages layer
ARG CACHEBUST=1

# Install Python dependencies (as airflow user)
RUN pip install --no-cache-dir \
    "snowflake-connector-python>=3.10.0" \
    "apache-airflow-providers-snowflake>=5.5.0" \
    "dbt-core>=1.8.0" \
    "dbt-snowflake>=1.8.0" \
    "astronomer-cosmos>=1.4.0" \
    && echo "✅ Installed Python packages:" \
    && pip list | grep -E "(snowflake|dbt|cosmos)"

# Set environment variables
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=true
ENV AIRFLOW__WEBSERVER__EXPOSE_CONFIG=true

# Create directories for dbt projects (as root, then change ownership)
USER root
RUN mkdir -p /opt/airflow/dags/dbt && \
    mkdir -p /opt/airflow/.dbt && \
    chown -R airflow:root /opt/airflow/dags/dbt && \
    chown -R airflow:root /opt/airflow/.dbt

# Switch back to airflow user for final setup
USER airflow
