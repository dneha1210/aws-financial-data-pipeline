import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job

# Job args
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Glue context setup
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ---------------------
# Load Silver Layer Data
# ---------------------

silver_path = "s3://nehaawsbc001/silver/"

customers = spark.read.parquet(f"{silver_path}/customers/")
loans = spark.read.parquet(f"{silver_path}/loans/")

# ---------------------
# Join and Aggregation
# ---------------------

# Join on customer_id
joined_df = loans.join(customers, on="customer_id", how="inner")

# Use customer_name directly
summary_df = joined_df.groupBy("customer_id", "customer_name") \
    .agg(
        count("loan_id").alias("total_loans"),
        avg("loan_amount").alias("avg_loan_amount")
    )

# ---------------------
# Write to Gold Layer
# ---------------------

gold_path = "s3://nehaawsbc001/gold/customer_loan_summary/"

summary_df.write.mode("overwrite").parquet(gold_path)

job.commit()
