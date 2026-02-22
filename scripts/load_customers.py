import pymysql
import snowflake.connector
import os
import pandas as pd

def transfer_customers():
    try:
        # 1. الاتصال بـ MySQL
        mysql_conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root_password_ci',
            database='ecommerce_db'
        )
        
        # 🔍 فحص: ما هي الجداول الموجودة فعلياً؟
        cursor = mysql_conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📋 Available tables in MySQL: {tables}")
        
        if not tables:
            print("⚠️ ALERT: No tables found in MySQL! Something is wrong with populate_data.py")
            return

        # سنحاول القراءة من أول جدول نجده (للفحص فقط)
        first_table = tables[0][0]
        print(f"📥 Attempting to read from table: {first_table}")
        df = pd.read_sql(f"SELECT * FROM {first_table} LIMIT 10", mysql_conn)
        
        # باقي كود Snowflake (كما هو)
        sf_conn = snowflake.connector.connect(
            user = os.getenv('TF_VAR_snowflake_user'),
            password = os.getenv('TF_VAR_snowflake_password'),
            account = os.getenv('TF_VAR_snowflake_account'),
            warehouse = 'ECOMMERCE_COMPUTE_WH',
            database = 'ECOMMERCE_RAW_DB',
            schema = 'LANDING_ZONE'
        )
        
        print(f"🚀 Found {len(df)} rows. Sending to Snowflake...")
        # (بقية عملية النقل...)
        
        sf_conn.close()
        mysql_conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    transfer_customers()
