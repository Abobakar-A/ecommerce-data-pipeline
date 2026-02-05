from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.utils.dates import days_ago
import pandas as pd

TABLES = ['customers', 'products', 'dates', 'sales']

# 1. الدالة الموحدة: تسحب من MySQL وتشحن لـ Snowflake فوراً
def extract_and_load(table_name):
    # أ. الاستخراج من MySQL
    mysql_hook = MySqlHook(mysql_conn_id='MYSQL_DEFAULT')
    df = mysql_hook.get_pandas_df(sql=f"SELECT * FROM {table_name}")
    print(f"Extracted {len(df)} rows from MySQL table: {table_name}")

    # ب. الشحن السريع لـ Snowflake
    snowflake_hook = SnowflakeHook(snowflake_conn_id='SNOWFLAKE_DEFAULT')
    engine = snowflake_hook.get_sqlalchemy_engine()
    
    df.to_sql(
        name=table_name.lower(), 
        con=engine, 
        schema='LANDING_ZONE',
        if_exists='replace', # استخدم replace للتنظيف أو append للإضافة
        index=False, 
        chunksize=5000, 
        method='multi' 
    )
    print(f"Successfully loaded {len(df)} rows to Snowflake table: {table_name}")

with DAG('complete_ecommerce_pipeline', start_date=days_ago(1), schedule_interval=None) as dag:
    
    load_tasks = []

    for table in TABLES:
        task = PythonOperator(
            task_id=f'load_{table}',
            python_callable=extract_and_load, # تأكد أن الاسم يطابق الدالة أعلاه
            op_kwargs={'table_name': table}
        )
        load_tasks.append(task)

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow/dbt_ecommerce && dbt run', 
    )

    load_tasks >> run_dbt