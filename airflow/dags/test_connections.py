from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime

def test_mysql():
    hook = MySqlHook(mysql_conn_id='mysql_default')
    conn = hook.get_conn()
    print("MySQL Connection Successful!")

def test_snowflake():
    hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
    conn = hook.get_conn()
    print("Snowflake Connection Successful!")

with DAG('test_my_connections', start_date=datetime(2026, 1, 1), schedule_interval=None, catchup=False) as dag:
    t1 = PythonOperator(task_id='test_mysql', python_callable=test_mysql)
    t2 = PythonOperator(task_id='test_snowflake', python_callable=test_snowflake)
    
    t1 >> t2