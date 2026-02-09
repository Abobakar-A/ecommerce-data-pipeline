FROM apache/airflow:2.7.1

USER root
# تثبيت git و libpq-dev (مهم جداً لربط مكتبات Postgres في بايثون)
RUN apt-get update && \
    apt-get install -y git libpq-dev gcc && \
    apt-get clean

USER airflow
# تثبيت المكتبات المطلوبة لـ Snowflake و Postgres و MySQL
RUN pip install --no-cache-dir \
    dbt-snowflake==1.7.0 \
    dbt-postgres==1.7.0 \
    faker \
    mysql-connector-python \
    pymysql \
    psycopg2-binary \
    pandas \
    sqlalchemy \
    requests

ENV PATH="${PATH}:/home/airflow/.local/bin"