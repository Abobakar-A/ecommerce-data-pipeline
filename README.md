
# 🚀 E-Commerce End-to-End Data Pipeline

An automated, modern data stack pipeline that synchronizes transactional data from a MySQL source to a Snowflake Data Warehouse, utilizing dbt for modeling and Airflow for orchestration.

## 📌 Project Overview
This project simulates a real-world E-commerce data environment. It handles everything from infrastructure provisioning and data ingestion to complex SQL transformations, resulting in a clean, query-ready **Star Schema**.



## 🏗️ Technical Architecture
* **Infrastructure:** `Terraform` (Infrastructure as Code) to manage Snowflake resources.
* **Orchestration:** `Apache Airflow` (Dockerized) to schedule and monitor the pipeline.
* **Source Database:** `MySQL` (Transactional data).
* **Data Warehouse:** `Snowflake` (Cloud storage and compute).
* **Transformation:** `dbt` (Data Build Tool) for modular, version-controlled SQL modeling.
* **Environment:** `Docker` & `GitHub Codespaces` for consistent development.

## 🛠️ Implementation Steps

### 1. Infrastructure Provisioning
Used **Terraform** to define the cloud environment. This included creating the `ECOMMERCE_RAW_DB` database, the `LANDING_ZONE` schema, and the compute warehouses in **Snowflake**.

### 2. Data Ingestion (ELT)
A custom **Airflow DAG** was developed to:
* Generate mock e-commerce data (Customers, Products, Sales).
* Populate a MySQL database.
* Automate the transfer of raw records from MySQL to the Snowflake Landing Zone.

### 3. Data Transformation (dbt)
Implemented a multi-layered modeling approach:
* **Staging Layer:** Cleaned raw data, handled case sensitivity, and renamed columns for consistency.
* **Core Layer:** Built the final **Star Schema** with optimized Dimension and Fact tables:
    * `dim_customers`: Verified customer profiles.
    * `dim_products`: Product categorization and pricing.
    * `dim_dates`: Time-dimension for temporal analysis.
    * `fact_sales`: Centralized sales transactions with metrics.



## 📂 Repository Structure
* `/terraform`: Snowflake infrastructure configuration (`.tf` files).
* `/dbt_ecommerce`: dbt project folder containing `models/staging` and `models/core`.
* `/airflow/dags`: Python scripts for pipeline orchestration.
* `/scripts`: SQL and Python scripts for data generation and database initialization.

## 🚀 Key Learning Outcomes
* **Integration:** Successfully linked disparate systems (MySQL → Airflow → Snowflake) using secure connectors.
* **Modeling:** Applied Dimensional Modeling techniques to turn raw logs into business insights.
* **Troubleshooting:** Resolved complex SQL compilation errors related to identifier case sensitivity and schema mismatches.

---
**Built by Abubakar - Data Engineering Portfolio Project**