SELECT
    DATE_ID,
    YEAR,
    MONTH,
    QUARTER,
    CURRENT_TIMESTAMP() AS STAGED_AT
FROM {{ source('ecommerce_raw', 'DIM_DATES') }}