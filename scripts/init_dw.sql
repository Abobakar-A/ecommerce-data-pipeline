-- 1. إنشاء الـ Schema
CREATE SCHEMA IF NOT EXISTS landing_zone;

-- 2. جدول التواريخ (المفقود)
CREATE TABLE IF NOT EXISTS landing_zone.dim_dates (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    quarter INT,
    day_name VARCHAR(20),
    is_weekend BOOLEAN
);

-- 3. جدول العملاء
CREATE TABLE IF NOT EXISTS landing_zone.dim_customers (
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255)
);

-- 4. جدول المنتجات
CREATE TABLE IF NOT EXISTS landing_zone.dim_products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    base_price FLOAT
);

-- 5. جدول المبيعات (المرتبط بالتواريخ)
CREATE TABLE IF NOT EXISTS landing_zone.fact_sales (
    sale_id INT PRIMARY KEY,
    date_id DATE, --REFERENCES landing_zone.dim_dates(date_id), -- ربط بجدول التواريخ
    customer_id INT,
    product_id INT,
    quantity INT,
    total_amount FLOAT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);