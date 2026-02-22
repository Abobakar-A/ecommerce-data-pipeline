import pymysql
import snowflake.connector
import os
import pandas as pd

def transfer_customers():
    try:
        # 1. الاتصال بـ MySQL (المصدر في GitHub)
        mysql_conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root_password_ci',
            database='ecommerce_db'
        )
        print("📥 Reading data from MySQL...")
        df = pd.read_sql("SELECT * FROM customers LIMIT 10", mysql_conn)
        
        # 2. الاتصال بـ Snowflake (المستودع في السحاب)
        sf_conn = snowflake.connector.connect(
            user = os.getenv('TF_VAR_snowflake_user'),
            password = os.getenv('TF_VAR_snowflake_password'),
            account = os.getenv('TF_VAR_snowflake_account'),
            warehouse = 'ECOMMERCE_COMPUTE_WH',
            database = 'ECOMMERCE_RAW_DB',
            schema = 'LANDING_ZONE'
        )
        
        # 3. تحويل البيانات لتناسب جدول Snowflake
        # نحن نحتاج (CUSTOMER_ID, FULL_NAME, EMAIL)
        sf_df = df[['id', 'name', 'email']].copy()
        sf_df.columns = ['CUSTOMER_ID', 'FULL_NAME', 'EMAIL']
        
        # 4. النقل
        print(f"🚀 Transferring {len(sf_df)} rows to Snowflake...")
        cursor = sf_conn.cursor()
        
        for index, row in sf_df.iterrows():
            sql = f"INSERT INTO DIM_CUSTOMERS (CUSTOMER_ID, FULL_NAME, EMAIL) VALUES ({row['CUSTOMER_ID']}, '{row['FULL_NAME']}', '{row['EMAIL']}')"
            cursor.execute(sql)
            
        print("✅ Data Loaded Successfully to DIM_CUSTOMERS!")
        
        cursor.close()
        sf_conn.close()
        mysql_conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    transfer_customers()
