import snowflake.connector
import os

# الاتصال باستخدام المفاتيح التي وضعناها في الـ Secrets
ctx = snowflake.connector.connect(
    user=os.getenv('TF_VAR_snowflake_user'),
    password=os.getenv('TF_VAR_snowflake_password'),
    account=os.getenv('TF_VAR_snowflake_account')
)

# تنفيذ أمر بسيط
cs = ctx.cursor()
cs.execute("SELECT CURRENT_TIMESTAMP()")
data = cs.fetchone()
print(f"✅ Connection Successful! Snowflake time is: {data[0]}")
