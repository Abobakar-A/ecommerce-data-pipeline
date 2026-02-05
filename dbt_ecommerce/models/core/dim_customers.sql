{{ config(materialized='table') }}

SELECT 
    CUSTOMER_ID,
    CUSTOMER_NAME AS FULL_NAME,
    EMAIL,
    STAGED_AT AS LOADED_AT
FROM {{ ref('stg_customers') }}