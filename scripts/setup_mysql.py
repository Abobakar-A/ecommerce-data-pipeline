import pandas as pd
from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime, timedelta



fake = Faker()

def setup_source_db():
    with engine.connect() as conn:
        # 1. إنشاء جدول العملاء
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                CUSTOMER_ID INT PRIMARY KEY,
                FULL_NAME VARCHAR(255),
                EMAIL VARCHAR(255)
            )
        """))
        
        # 2. إنشاء جدول المنتجات
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                PRODUCT_ID INT PRIMARY KEY,
                PRODUCT_NAME VARCHAR(255),
                CATEGORY VARCHAR(100),
                BASE_PRICE FLOAT
            )
        """))

        # 3. إنشاء جدول التواريخ
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dates (
                DATE_ID DATE PRIMARY KEY,
                YEAR INT,
                MONTH INT,
                QUARTER INT
            )
        """))

        # 4. إنشاء جدول المبيعات (Fact)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sales (
                SALE_ID INT PRIMARY KEY,
                DATE_ID DATE,
                CUSTOMER_ID INT,
                PRODUCT_ID INT,
                QUANTITY INT,
                TOTAL_AMOUNT FLOAT
            )
        """))
    print("✅ تم إنشاء الجداول الأربعة في MySQL بنجاح!")

if __name__ == "__main__":
    setup_source_db()