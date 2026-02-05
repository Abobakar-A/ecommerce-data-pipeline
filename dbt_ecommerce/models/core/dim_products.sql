{{ config(materialized='table') }}

SELECT 
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    BASE_PRICE,
    STAGED_AT AS LOADED_AT
FROM {{ ref('stg_products') }}