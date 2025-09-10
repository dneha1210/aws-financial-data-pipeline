# AWS Financial Data Pipeline – Customer Analytics

##  Overview
This project implements a **scalable financial data pipeline** for a retail banking use case.  
It processes raw customer, account, loan, and transaction data into **analytics-ready datasets** while enabling **risk prediction** using machine learning.

##  Objectives
- Detect potential **loan defaults** early  
- Enable **customer personalization** (product recommendations)  
- Support **fraud detection & compliance reporting**  
- Build a **scalable & cost-efficient data pipeline** on AWS  

---

##  Architecture
The solution follows the **Medallion Architecture**:

1. **Bronze Layer (Raw Ingestion)** – Raw CSV data stored in S3 (via Terraform).  
2. **Silver Layer (Cleansed Data)** – AWS Glue ETL (PySpark) cleans and standardizes data.  
3. **Gold Layer (Business Analytics)** – Aggregated, business-ready data for Athena/QuickSight.  

![Architecture Diagram](architecture/medallion_architecture.png)

---

##  Tech Stack
- **Infrastructure:** Terraform + AWS IAM + S3  
- **ETL:** AWS Glue (PySpark)  
- **Data Catalog:** Glue Crawler  
- **Query Engine:** Amazon Athena  
- **ML/Analytics:** Databricks (Logistic Regression with PySpark), AWS QuickSight  
- **Storage Format:** Parquet (optimized for analytics)  

---

##  Workflow
1. **Terraform** provisions S3 buckets with Bronze, Silver, and Gold zones.  
2. **Glue Jobs**  
   - Bronze → Silver: Cleaning, deduplication, schema enforcement.  
   - Silver → Gold: Joins + aggregations (loan summary per customer).  
3. **Glue Crawler** updates Data Catalog.  
4. **Athena Queries** used for business reporting.  
5. **ML Pipeline** in Databricks trains a Logistic Regression model for loan default risk.  
6. **Visualization** in QuickSight dashboard.  

---

##  Security & Compliance
- IAM roles for Glue & Athena (least privilege)  
- S3 bucket policies with encryption  
- Clear lineage from Bronze → Silver → Gold  
- PII handled securely (customer IDs preserved, no duplication)  

---

##  Results
- **Gold Layer dataset:** Customer loan summaries (loan counts & avg amounts).  
- **ML Model:** Logistic Regression trained with PySpark; ROC-AUC evaluated in Databricks.  
- **Dashboard:** QuickSight visualization for risk monitoring.  

---

##  Future Improvements
- Automate alerting with **Lambda + Athena + SNS** for high-risk customers  
- Integrate with **real-time streaming (Kinesis)** for transaction monitoring  
- Deploy ML model as an **API endpoint** for real-time scoring  

---

