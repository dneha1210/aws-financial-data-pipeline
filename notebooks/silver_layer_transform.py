import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, to_date, to_timestamp
from pyspark.sql.types import IntegerType, DoubleType
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job

# Job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Glue context and Spark session
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ----------------------
# Read Raw Bronze Data
# ----------------------

bronze_path = "s3://nehaawsbc001/bronze/"

# Read each CSV file
customers_df = spark.read.option("header", "true").csv(f"{bronze_path}/customers.csv")
accounts_df = spark.read.option("header", "true").csv(f"{bronze_path}/accounts.csv")
transactions_df = spark.read.option("header", "true").csv(f"{bronze_path}/transactions.csv")
loans_df = spark.read.option("header", "true").csv(f"{bronze_path}/loans.csv")
loan_payments_df = spark.read.option("header", "true").csv(f"{bronze_path}/loan_payments.csv")

# ----------------------
# Cleaning and Transformation
# ----------------------

# Clean customers
customers_clean = customers_df.dropDuplicates(["customer_id"]).na.drop(subset=["customer_id"])
customers_clean = customers_clean.withColumn("customer_id", col("customer_id").cast("string")) \
                                 .withColumn("email", trim(col("email"))) \
                                 .withColumn("date_joined", to_date("date_joined", "yyyy-MM-dd"))

# Clean accounts
accounts_clean = accounts_df.dropDuplicates(["account_id"]) \
                             .withColumn("account_id", col("account_id").cast("string")) \
                             .withColumn("customer_id", col("customer_id").cast("string")) \
                             .withColumn("balance", col("balance").cast(DoubleType()))

# Clean transactions
transactions_clean = transactions_df.dropDuplicates(["transaction_id"]) \
    .withColumn("transaction_id", col("transaction_id").cast("string")) \
    .withColumn("account_id", col("account_id").cast("string")) \
    .withColumn("amount", col("amount").cast(DoubleType())) 

# Clean loans
loans_clean = loans_df.dropDuplicates(["loan_id"]) \
    .withColumn("loan_id", col("loan_id").cast("string")) \
    .withColumn("customer_id", col("customer_id").cast("string")) \
    .withColumn("loan_amount", col("loan_amount").cast(DoubleType()))

# Clean loan payments
loan_payments_clean = loan_payments_df.dropDuplicates(["payment_id"]) \
    .withColumn("payment_id", col("payment_id").cast("string")) \
    .withColumn("loan_id", col("loan_id").cast("string")) \
    .withColumn("payment_amount", col("payment_amount").cast(DoubleType())) 

# ----------------------
# Write to Silver Layer
# ----------------------

silver_path = "s3://nehaawsbc001/silver/"

customers_clean.write.mode("overwrite").parquet(f"{silver_path}/customers/")
accounts_clean.write.mode("overwrite").parquet(f"{silver_path}/accounts/")
transactions_clean.write.mode("overwrite").parquet(f"{silver_path}/transactions/")
loans_clean.write.mode("overwrite").parquet(f"{silver_path}/loans/")
loan_payments_clean.write.mode("overwrite").parquet(f"{silver_path}/loan_payments/")

job.commit()
