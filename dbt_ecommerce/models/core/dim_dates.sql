{{ config(materialized='table') }}

SELECT
    DATE_ID,
    YEAR,
    MONTH,
    QUARTER,
    STAGED_AT AS LOADED_AT
FROM {{ ref('stg_dates') }}