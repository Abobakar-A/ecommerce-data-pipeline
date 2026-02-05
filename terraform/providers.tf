terraform {
  required_providers {
    snowflake = {
      # هذا هو المسار الصحيح للمزود
      source  = "snowflakedb/snowflake"
      version = "~> 0.87.0"
    }
  }
}

provider "snowflake" {
  account  = var.snowflake_account
  user     = var.snowflake_user
  password = var.snowflake_password
  role     = "ACCOUNTADMIN"
}