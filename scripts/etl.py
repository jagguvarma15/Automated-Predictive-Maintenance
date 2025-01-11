import os
import boto3
from pyspark.sql import SparkSession

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
try:
    raw_data = spark.read.csv(input_path, header=True, inferSchema=True)
    print("Raw data loaded successfully.")
except Exception as e:
    print(f"Failed to load raw data: {e}")
    exit(1)

# Inspect schema for debugging
raw_data.printSchema()

# Step 2: Data transformation
try:
    transformed_data = raw_data.selectExpr(
        "timestamp as timestamp",
        "cast(DV_pressure as double) as pressure",
        "cast(Oil_temperature as double) as temperature",
        "cast(Motor_current as double) as motor_current",
        "cast(COMP as int) as air_intake"
    )
    print("Data transformation completed.")
except Exception as e:
    print(f"Data transformation failed: {e}")
    exit(1)

# Step 3: Write processed data to local directory
try:
    os.makedirs(os.path.dirname(local_output_path), exist_ok=True)  # Ensure the processed directory exists
    transformed_data.write.parquet(local_output_path, mode="overwrite")
    print(f"Processed data saved locally at: {local_output_path}")
except Exception as e:
    print(f"Failed to save processed data locally: {e}")
    exit(1)

# Step 4: Upload processed data to S3
s3 = boto3.client("s3", region_name="us-east-1")


def upload_to_s3(local_path, bucket_name, s3_key_prefix):
    """
    Upload processed data to the specified S3 bucket and path.

    Args:
        local_path (str): Local file path to upload.
        bucket_name (str): Name of the S3 bucket.
        s3_key_prefix (str): Prefix for the S3 key.
    """
    for root, _, files in os.walk(os.path.dirname(local_path)):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_key = f"{s3_key_prefix}{file}"  # Example: data/processed/MetroPT3_cleaned.parquet
            try:
                s3.upload_file(local_file_path, bucket_name, s3_key)
                print(f"Uploaded {file} to s3://{bucket_name}/{s3_key}")
            except boto3.exceptions.S3UploadFailedError as e:
                print(f"Failed to upload {file}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during upload: {e}")


# Call the upload function
try:
    upload_to_s3(local_output_path, bucket_name, s3_key_prefix)
    print("All files uploaded to S3 successfully.")
except Exception as e:
    print(f"Failed to upload processed data to S3: {e}")
    exit(1)
