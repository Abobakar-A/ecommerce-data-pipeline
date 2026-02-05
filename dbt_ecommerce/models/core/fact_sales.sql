{{ config(materialized='table') }}

SELECT 
    SALE_ID,
    CUSTOMER_ID,
    PRODUCT_ID,
    DATE_ID,
    QUANTITY,
    TOTAL_AMOUNT,
    STAGED_AT AS LOADED_AT
FROM {{ ref('stg_sales') }}