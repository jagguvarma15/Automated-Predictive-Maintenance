import boto3
import pandas as pd
import os

# AWS S3 configuration
s3 = boto3.client('s3')
bucket_name = "raw-data-apm"
file_name = "MetroPT3(AirCompressor).csv"  # Local file name
s3_key = "MetroPT3(AirCompressor).csv"    # Key (path) in the S3 bucket

# Load MetroPT-3 dataset locally
data = pd.read_csv("/workspaces/Automated-Predictive-Maintenance/MetroPT3(AirCompressor).csv")

# Save the data locally as a CSV file (if needed for debugging or validation)
data.to_csv(file_name, index=False)

# Ensure the directory exists
raw_data_dir = "/workspaces/Automated-Predictive-Maintenance/data/raw/"
os.makedirs(raw_data_dir, exist_ok=True)

# Save the data into the raw directory
raw_file_path = os.path.join(raw_data_dir, file_name)
data.to_csv(raw_file_path, index=False)
print(f"Saved updated dataset to: {raw_file_path}")

# Upload dataset to S3
try:
    s3.upload_file(file_name, bucket_name, s3_key)  # Key instead of full S3 URI
    print(f"Uploaded {file_name} to s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"Failed to upload file: {e}")
