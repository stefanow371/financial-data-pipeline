# Financial Data Platform (dbt + BigQuery)

## Overview
This project demonstrates a production-grade **Modern Data Stack** architecture designed to transform raw financial data into actionable business insights. Using **dbt (data build tool)** and **Google BigQuery**, I have implemented a modular data pipeline that follows the **Medallion Architecture** to ensure data reliability, lineage, and performance.

The primary goal is to solve typical corporate finance challenges: **Budget vs. Actual analysis**, **Burn Rate tracking**, and **Currency impact normalization**.

Project is currently in progress and may not be complete.

---

##  Tech Stack
* **Data Warehouse:** Google BigQuery
* **Transformation:** dbt (Core)
* **Ingestion:** Python (Pandas & Google Cloud SDK)
* **Orchestration:** GitHub Actions (CI/CD)
* **Environment:** Docker

---

## Data Architecture (Medallion Model) 
The pipeline is structured into logical layers to ensure high data quality and maintainability:

1.  **Bronze (Staging):** Direct mapping of raw ingestion tables. Focus: schema enforcement, field renaming (standardization), and initial type casting.
2.  **Silver (Intermediate):** Implementation of core business logic. This layer handles currency conversions, deduplication, and complex joins between transactions and cost center metadata.
3.  **Gold (Marts):** Final, highly-optimized "Reporting" layer. Pre-calculated KPIs such as *Variance to Budget* and *YTD Spend*, ready for consumption by BI tools (Power BI/Looker).

---

## Key Engineering Features
* **Incremental Modeling:** Optimized BigQuery compute costs by implementing incremental refresh strategies for large-scale transaction tables.
* **Data Quality Guardrails:** Built-in data validation using `dbt-tests` (testing for uniqueness, null values, and custom financial logic).
* **Cost Optimization:** Leveraged BigQuery-native features like **Partitioning** (by transaction date) and **Clustering** (by cost center) to minimize query execution time and costs.
* **Data Lineage & Docs:** Automated documentation and visual lineage tracking using `dbt docs`.

---

## Business Use Case: Budget Variance
The platform automates the detection of budget overruns. By integrating `fct_transactions` with `dim_budgets`, the system automatically flags any cost center exceeding its monthly allocated limit by more than 10%, allowing for proactive financial management and faster month-end closing.

---

## How to Run

### Prerequisites
* Docker & Docker Compose
* Google Cloud Service Account (JSON key) with BigQuery Admin permissions

### Setup & Execution
1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/stefanow371/financial-data-pipeline.git](https://github.com/stefanow371/financial-data-pipeline.git)
    cd financial-data-pipeline
    ```

2.  **Environment Setup:**
    Place your GCP credentials in the `credentials/` folder and update `profiles.yml`.

3.  **Run Pipeline:**
    ```bash
    # Build and start the environment
    docker-compose up -d

    # Run dbt models
    dbt seed  # Load static
