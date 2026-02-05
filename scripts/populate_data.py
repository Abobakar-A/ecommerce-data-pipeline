import os
import pandas as pd
from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 1. تحميل الإعدادات من ملف .env
load_dotenv()

DB_USER = os.getenv("MYSQL_USER", "user")
DB_PASS = os.getenv("MYSQL_PASSWORD", "password")
DB_HOST = "127.0.0.1"  # للوصول من الـ venv إلى حاوية Docker
DB_PORT = "3306"
DB_NAME = os.getenv("MYSQL_DATABASE", "ecommerce_db")

# 2. إنشاء محرك الاتصال (Engine)
# نتصل أولاً بدون تحديد قاعدة بيانات للتأكد من وجودها
base_url = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}'
temp_engine = create_engine(base_url)

try:
    with temp_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        print(f"✅ تم التأكد من وجود قاعدة البيانات: {DB_NAME}")
except Exception as e:
    print(f"⚠️ تنبيه عند إنشاء القاعدة: {e}")

# الاتصال بالقاعدة المستهدفة
engine = create_engine(f"{base_url}/{DB_NAME}")
fake = Faker()

print("⏳ جاري توليد بيانات متوافقة مع Snowflake Schema...")

# --- توليد البيانات لتطابق جداول Terraform ---

# 1. جدول العملاء (DIM_CUSTOMERS)
customers = pd.DataFrame([{
    "CUSTOMER_ID": i,
    "FULL_NAME": fake.name(),
    "EMAIL": fake.email()
} for i in range(1, 1001)])

# 2. جدول المنتجات (DIM_PRODUCTS)
products_list = [
    ('MacBook Pro', 'Electronics', 2400.0), ('iPhone 15', 'Electronics', 999.0),
    ('Coffee Machine', 'Home', 150.0), ('Vacuum Cleaner', 'Home', 300.0),
    ('Running Shoes', 'Fashion', 120.0), ('Leather Jacket', 'Fashion', 250.0)
]
products = pd.DataFrame([{
    "PRODUCT_ID": i + 1,
    "PRODUCT_NAME": p[0],
    "CATEGORY": p[1],
    "BASE_PRICE": p[2]
} for i, p in enumerate(products_list)])

# 3. جدول التواريخ (DIM_DATES)
start_date = datetime(2025, 1, 1)
dates = pd.DataFrame([{
    "DATE_ID": (start_date + timedelta(days=x)).date(),
    "YEAR": (start_date + timedelta(days=x)).year,
    "MONTH": (start_date + timedelta(days=x)).month,
    "QUARTER": ((start_date + timedelta(days=x)).month - 1) // 3 + 1
} for x in range(365)])

# 4. جدول المبيعات (FACT_SALES)
sales = []
for i in range(1, 5001):
    product = products.sample(1).iloc[0]
    qty = random.randint(1, 5)
    sales.append({
        "SALE_ID": i,
        "DATE_ID": random.choice(dates['DATE_ID'].tolist()),
        "CUSTOMER_ID": random.randint(1, 1000),
        "PRODUCT_ID": product["PRODUCT_ID"],
        "QUANTITY": qty,
        "TOTAL_AMOUNT": round(float(qty * product["BASE_PRICE"]), 2)
    })
fact_sales = pd.DataFrame(sales)

# 3. ضخ البيانات إلى MySQL
print("🚀 جاري ضخ البيانات إلى الجداول الأربعة...")

tables = {
    'customers': customers,
    'products': products,
    'dates': dates,
    'sales': fact_sales
}

for table_name, df in tables.items():
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"✅ تم شحن جدول: {table_name} ({len(df)} سجل)")

print("\n✨ انتهى! MySQL الآن ممتلئة بالبيانات وجاهزة للـ Airflow Pipeline.")