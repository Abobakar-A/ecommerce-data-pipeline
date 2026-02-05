# إنشاء قاعدة بيانات للبيانات الخام
resource "snowflake_database" "raw_db" {
  name = "ECOMMERCE_RAW_DB"
}

# إنشاء مستودع (Warehouse) للمعالجة
resource "snowflake_warehouse" "wh" {
  name           = "ECOMMERCE_COMPUTE_WH"
  warehouse_size = "X-Small"
  auto_suspend   = 60
}

# إنشاء Schema داخل قاعدة البيانات
resource "snowflake_schema" "raw_schema" {
  database = snowflake_database.raw_db.name
  name     = "LANDING_ZONE"
}
# 1. Dimension: Customers
resource "snowflake_table" "dim_customers" {
  database = snowflake_database.raw_db.name
  schema   = snowflake_schema.raw_schema.name
  name     = "DIM_CUSTOMERS"

  column {
    name = "CUSTOMER_ID"
    type = "NUMBER"
  }
  column {
    name = "FULL_NAME"
    type = "STRING"
  }
  column {
    name = "EMAIL"
    type = "STRING"
  }
}

# 2. Dimension: Products
resource "snowflake_table" "dim_products" {
  database = snowflake_database.raw_db.name
  schema   = snowflake_schema.raw_schema.name
  name     = "DIM_PRODUCTS"

  column {
    name = "PRODUCT_ID"
    type = "NUMBER"
  }
  column {
    name = "PRODUCT_NAME"
    type = "STRING"
  }
  column {
    name = "CATEGORY"
    type = "STRING"
  }
  column {
    name = "BASE_PRICE"
    type = "FLOAT"
  }
}

# 3. Dimension: Dates
resource "snowflake_table" "dim_dates" {
  database = snowflake_database.raw_db.name
  schema   = snowflake_schema.raw_schema.name
  name     = "DIM_DATES"

  column {
    name = "DATE_ID"
    type = "DATE"
  }
  column {
    name = "YEAR"
    type = "NUMBER"
  }
  column {
    name = "MONTH"
    type = "NUMBER"
  }
  column {
    name = "QUARTER"
    type = "NUMBER"
  }
}

# 4. FACT Table: Sales
resource "snowflake_table" "fact_sales" {
  database = snowflake_database.raw_db.name
  schema   = snowflake_schema.raw_schema.name
  name     = "FACT_SALES"

  column {
    name = "SALE_ID"
    type = "NUMBER"
  }
  column {
    name = "DATE_ID"
    type = "DATE"
  }
  column {
    name = "CUSTOMER_ID"
    type = "NUMBER"
  }
  column {
    name = "PRODUCT_ID"
    type = "NUMBER"
  }
  column {
    name = "QUANTITY"
    type = "NUMBER"
  }
  column {
    name = "TOTAL_AMOUNT"
    type = "FLOAT"
  }
  column {
    name = "LOADED_AT"
    type = "TIMESTAMP_NTZ"
    default {
      expression = "CURRENT_TIMESTAMP()"
    }
  }
}