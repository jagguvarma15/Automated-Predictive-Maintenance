from pyspark.sql import SparkSession
import boto3
import os

# Initialize Spark session
spark = SparkSession.builder \
    .appName("ETL for MetroPT3 Dataset") \
    .getOrCreate()

# Input and output paths
input_path = "/workspaces/Automated-Predictive-Maintenance/data/raw/MetroPT3(AirCompressor).csv"
local_output_path = "/workspaces/Automated-Predictive-Maintenance/data/processed/MetroPT3_cleaned.parquet"
bucket_name = "raw-data-apm"
s3_key_prefix = "data/processed/"

# Step 1: Read the raw data
raw_data = spark.read.csv(input_path, header=True, inferSchema=True)

# Inspect schema for debugging
raw_data.printSchema()

# Step 2: Data transformation
transformed_data = raw_data.selectExpr(
    "timestamp as timestamp",
    "cast(DV_pressure as double) as pressure",
    "cast(Oil_temperature as double) as temperature",
    "cast(Motor_current as double) as motor_current",
    "cast(COMP as int) as air_intake"
)

# Step 3: Write processed data to local directory
os.makedirs(os.path.dirname(local_output_path), exist_ok=True)  # Ensure the local processed directory exists
transformed_data.write.parquet(local_output_path, mode="overwrite")
print(f"Processed data saved locally at: {local_output_path}")

# Step 4: Upload processed data to S3
s3 = boto3.client('s3', region_name='us-east-1')

def upload_to_s3(local_path, bucket_name, s3_key_prefix):
    """
    Upload processed data to the specified S3 bucket and path.
    """
    for root, _, files in os.walk(os.path.dirname(local_path)):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_key = f"{s3_key_prefix}{file}"  # Example: data/processed/MetroPT3_cleaned.parquet
            try:
                s3.upload_file(local_file_path, bucket_name, s3_key)
                print(f"Uploaded {file} to s3://{bucket_name}/{s3_key}")
            except Exception as e:
                print(f"Failed to upload {file}: {e}")

# Call the upload function
upload_to_s3(local_output_path, bucket_name, s3_key_prefix)
