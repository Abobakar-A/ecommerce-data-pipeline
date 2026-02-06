from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.utils.dates import days_ago
import pandas as pd
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
import json
# دالة التنبيه عند الفشل
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

def send_slack_notification(**context):
    dag_id = context.get('task_instance').dag_id
    task_id = context.get('task_instance').task_id
    execution_date = context.get('execution_date')
    log_url = context.get('task_instance').log_url
    state = context.get('task_instance').state

    # اختيار الأيقونة بناءً على الحالة
    icon = "✅" if state == 'success' else "🔴"
    status_text = "All tasks are GOOD!" if state == 'success' else "Task FAILED!"

    slack_msg = f"""
    {icon} *Pipeline Notification*
    *Status:* {status_text}
    *DAG:* {dag_id}
    *Task:* {task_id}
    *Time:* {execution_date}
    *Logs:* <{log_url}|Click here to view logs>
    """
    
    # إرسال التنبيه
    alert = SlackWebhookOperator(
        task_id='slack_notification',
        slack_webhook_conn_id='slack_conn', # سنقوم بتعريفه في واجهة Airflow
        message=slack_msg,
        channel='#kokoslm1400' # اسم القناة في Slack
    )
    return alert.execute(context=context)

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

with DAG(
    'complete_ecommerce_pipeline',
    start_date=days_ago(1),
    schedule_interval= '@hourly',
    catchup=False,
    on_failure_callback=send_slack_notification, # يعمل تلقائياً عند فشل أي مهمة
    default_args={
        'retries': 1,
    }
) as dag:
    
    load_tasks = []

    for table in TABLES:
        task = PythonOperator(
            task_id=f'load_{table}',
            python_callable=extract_and_load,
            op_kwargs={'table_name': table}
        )
        load_tasks.append(task)
    run_dbt_tests = BashOperator(
    task_id='run_dbt_tests',
    bash_command='cd /opt/airflow/dbt_ecommerce && dbt test',
   )   

    run_dbt = BashOperator(
    task_id='run_dbt_models',
    bash_command='cd /opt/airflow/dbt_ecommerce && dbt run', 
    )
    notify_success = PythonOperator(
        task_id='notify_success',
        python_callable=send_slack_notification,
        provide_context=True,
        trigger_rule='all_success' # لا تعمل إلا إذا نجح كل شيء قبلها
    )

    load_tasks >> run_dbt >> run_dbt_tests >> notify_success