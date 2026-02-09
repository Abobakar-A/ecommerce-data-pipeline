from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import pandas as pd
import requests

# دالة التنبيه عبر Slack (بسيطة ومستقرة)
def send_slack_notification(**kwargs):
    webhook_url = "https://hooks.slack.com/services/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"
    ti = kwargs.get('task_instance')
    state = ti.state
    icon = "✅" if state == 'success' else "🔴"
    
    payload = {
        "text": f"{icon} *Pipeline Update*\n*DAG:* {ti.dag_id}\n*Task:* {ti.task_id}\n*Status:* {state}\n<{ti.log_url}|View Logs>"
    }
    try:
        requests.post(webhook_url, json=payload, timeout=10)
    except:
        pass

TABLES = ['DIM_CUSTOMERS', 'DIM_PRODUCTS', 'DIM_DATES', 'FACT_SALES']

def extract_and_load(table_name):
    mysql_hook = MySqlHook(mysql_conn_id='mysql_default')
    df = mysql_hook.get_pandas_df(sql=f"SELECT * FROM {table_name}")
    
    snowflake_hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
    engine = snowflake_hook.get_sqlalchemy_engine()

    pg_hook = PostgresHook(postgres_conn_id='postgres_dw')
    engine_pg = pg_hook.get_sqlalchemy_engine()
    df.to_sql(
        name=table_name.lower(),
        con=engine_pg,
        schema='landing_zone',
        if_exists='replace',
        index=False
    )
    
    df.to_sql(
        name=table_name.lower(), 
        con=engine, 
        schema='LANDING_ZONE',
        if_exists='replace',
        index=False, 
        method='multi' 
    )

with DAG(
    'complete_ecommerce_pipeline',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    on_failure_callback=send_slack_notification
) as dag:

    # 1. توليد البيانات (نقطة البداية)
    generate_data = BashOperator(
        task_id='generate_mysql_data',
        bash_command='python /opt/airflow/scripts/populate_data.py'
    )

    # 2. نقل البيانات
    load_tasks = []
    for table in TABLES:
        task = PythonOperator(
            task_id=f'load_{table}',
            python_callable=extract_and_load,
            op_kwargs={'table_name': table}
        )
        load_tasks.append(task)

    # 3. تشغيل dbt
    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command="cd /opt/airflow/dbt_ecommerce && dbt run --profiles-dir ."
    )

    # 4. اختبار dbt
    run_dbt_tests = BashOperator(
        task_id='run_dbt_tests',
        bash_command="cd /opt/airflow/dbt_ecommerce && dbt test --profiles-dir ."
    )

    # 5. تنبيه النجاح
    notify_success = PythonOperator(
        task_id='notify_success',
        python_callable=send_slack_notification,
        provide_context=True,
        trigger_rule='all_success',
    )

    generate_data >> load_tasks >> run_dbt >> run_dbt_tests >> notify_success