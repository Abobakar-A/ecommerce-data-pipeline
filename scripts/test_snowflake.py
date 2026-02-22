import snowflake.connector
import os

def check_my_tables():
    try:
        # الاتصال باستخدام المفاتيح
        ctx = snowflake.connector.connect(
            user=os.getenv('TF_VAR_snowflake_user'),
            password=os.getenv('TF_VAR_snowflake_password'),
            account=os.getenv('TF_VAR_snowflake_account'),
            warehouse='ECOMMERCE_COMPUTE_WH', # المحرك الذي أنشأناه
            database='ECOMMERCE_RAW_DB',      # قاعدة البيانات
            schema='LANDING_ZONE'             # المخطط
        )
        
        cs = ctx.cursor()
        
        # أمر لسرد الجداول الموجودة
        print("🔍 Checking tables in ECOMMERCE_RAW_DB.LANDING_ZONE...")
        cs.execute("SHOW TABLES")
        
        tables = cs.fetchall()
        
        if not tables:
            print("⚠️ No tables found. Maybe Terraform hasn't run 'Apply' yet?")
        else:
            print(f"✅ Success! Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[1]} (Created on: {table[2]})")
                
        cs.close()
        ctx.close()
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    check_my_tables()
