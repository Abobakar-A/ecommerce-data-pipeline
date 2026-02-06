{{ config(
    materialized='view'
) }}

WITH sales AS (
    SELECT * FROM {{ ref('stg_sales') }}
),
customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),
products AS (
    SELECT * FROM {{ ref('stg_products') }}
)

SELECT 
    s.SALE_ID,
    s.DATE_ID AS SALE_DATE,    
    s.TOTAL_AMOUNT,
    s.QUANTITY,
    c.CUSTOMER_NAME,
    c.EMAIL,
    p.PRODUCT_NAME,
    p.CATEGORY
FROM sales s
JOIN customers c ON s.CUSTOMER_ID = c.CUSTOMER_ID
JOIN products p ON s.PRODUCT_ID = p.PRODUCT_ID