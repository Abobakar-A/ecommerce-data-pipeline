import os
import pandas as pd
from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime, timedelta

# 1. سحب الإعدادات (استخدام الأسماء الصحيحة من ملف .env)
DB_USER = "root"
DB_PASS = os.getenv("MYSQL_ROOT_PASSWORD") 
DB_HOST = "mysql"  # هذا هو اسم "الخدمة" في docker-compose
DB_PORT = "3306"
DB_NAME = os.getenv("MYSQL_DB_NAME") # تأكد من وجود _NAME كما في .env
NORMAL_USER = os.getenv("MYSQL_USER")

if not DB_PASS:
    print("❌ خطأ: لم يتم العثور على MYSQL_ROOT_PASSWORD")
    exit(1)

# 2. إنشاء محرك الاتصال (Engine)
# نستخدم mysql_ecommerce كاسم مضيف (Host) إذا كان اسم الخدمة في YAML هو mysql
base_url = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}'
engine_root = create_engine(base_url)

try:
    with engine_root.connect() as conn:
        # تنفيذ الأوامر يدوياً لضمان الصلاحيات
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.execute(text(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{NORMAL_USER}'@'%'"))
        conn.execute(text("FLUSH PRIVILEGES"))
        conn.commit()
        print(f"✅ تم تهيئة القاعدة {DB_NAME} بنجاح.")
except Exception as e:
    print(f"⚠️ تنبيه أثناء التهيئة: {e}")

# إنشاء محرك الاتصال للقاعدة المستهدفة
engine = create_engine(f"{base_url}/{DB_NAME}")
fake = Faker()

print("⏳ جاري توليد البيانات...")

# --- توليد البيانات (نفس منطقك الرائع) ---
customers = pd.DataFrame([{"CUSTOMER_ID": i, "FULL_NAME": fake.name(), "EMAIL": fake.email()} for i in range(1, 1001)])

products_list = [('MacBook Pro', 'Electronics', 2400.0), ('iPhone 15', 'Electronics', 999.0),
                 ('Coffee Machine', 'Home', 150.0), ('Vacuum Cleaner', 'Home', 300.0),
                 ('Running Shoes', 'Fashion', 120.0), ('Leather Jacket', 'Fashion', 250.0)]
products = pd.DataFrame([{"PRODUCT_ID": i + 1, "PRODUCT_NAME": p[0], "CATEGORY": p[1], "BASE_PRICE": p[2]} for i, p in enumerate(products_list)])

start_date = datetime(2025, 1, 1)
dates = pd.DataFrame([{
    "DATE_ID": (start_date + timedelta(days=x)).date(),
    "YEAR": (start_date + timedelta(days=x)).year,
    "MONTH": (start_date + timedelta(days=x)).month,
    "QUARTER": ((start_date + timedelta(days=x)).month - 1) // 3 + 1
} for x in range(365)])

sales = []
for i in range(1, 2001):
    prod = products.sample(1).iloc[0]
    qty = random.randint(1, 3)
    sales.append({
        "SALE_ID": i,
        "DATE_ID": random.choice(dates['DATE_ID'].tolist()),
        "CUSTOMER_ID": random.randint(1, 1000),
        "PRODUCT_ID": prod["PRODUCT_ID"],
        "QUANTITY": qty,
        "TOTAL_AMOUNT": round(float(qty * prod["BASE_PRICE"]), 2)
    })
fact_sales = pd.DataFrame(sales)

# 3. ضخ البيانات (بأحرف كبيرة لتطابق الـ DAG)
tables = {
    'DIM_CUSTOMERS': customers, 
    'DIM_PRODUCTS': products,
    'DIM_DATES': dates,
    'FACT_SALES': fact_sales
}

for table_name, df in tables.items():
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"✅ تم شحن جدول: {table_name}")

print("\n✨ MySQL جاهزة للعمل!")