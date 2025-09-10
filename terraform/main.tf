terraform {
required_providers {
aws = {
source = "hashicorp/aws"
version = "~> 5.0"
}
}
}
provider "aws" {
region = "us-east-1"
access_key = "INSERT-YOUR-ACCESS-KEY"
secret_key = "INSERT-YOUR-SECRET-KEY"
}
# Step 1: Create the S3 bucket
resource "aws_s3_bucket" "data_lake" {
bucket = "neha-bc001project"
tags = {
Name = "Data Lake Bucket"
}
}
# Step 2: Upload files into 'bronze/' layer with correct keys
resource "aws_s3_object" "bronze_accounts" {
bucket = aws_s3_bucket.data_lake.id
key = "bronze/accounts.csv"
source = "INSERT-LOCATION-OF-CSV"
content_type = "text/csv"
}
resource "aws_s3_object" "bronze_customers" {
bucket = aws_s3_bucket.data_lake.id
key = "bronze/customers.csv"
source = "INSERT-LOCATION-OF-CSV"
content_type= "text/csv"
}
resource "aws_s3_object" "bronze_loans" {
bucket = aws_s3_bucket.data_lake.id
key = "bronze/loans.csv"
source = "INSERT-LOCATION-OF-CSV"
content_type = "text/csv"
}
resource "aws_s3_object" "bronze_loan_payments" {
bucket = aws_s3_bucket.data_lake.id
key = "bronze/loan_payments.csv"
source = "INSERT-LOCATION-OF-CSV"
content_type = "text/csv"
}
resource "aws_s3_object" "bronze_transactions" {
bucket = aws_s3_bucket.data_lake.id
key = "bronze/transactions.csv"
source = "INSERT-LOCATION-OF-CSV"
content_type = "text/csv"
}
# Step 3: Create empty 'silver/' and 'gold/' folders (optional)
resource "aws_s3_object" "silver_layer" {
bucket = aws_s3_bucket.data_lake.id
key = "silver/"
content = ""
}
resource "aws_s3_object" "gold_layer" {
bucket = aws_s3_bucket.data_lake.id
key = "gold/"
content = ""
}
