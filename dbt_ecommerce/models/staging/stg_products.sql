SELECT
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    BASE_PRICE, -- تم التصحيح من PRICE إلى BASE_PRICE
    CURRENT_TIMESTAMP() AS STAGED_AT
FROM {{ source('ecommerce_raw', 'PRODUCTS') }}