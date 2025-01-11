import boto3
import pandas as pd
import os
import requests
import zipfile
from io import BytesIO

# AWS S3 configuration
s3 = boto3.client('s3')
bucket_name = "raw-data-apm"
s3_key = "MetroPT3(AirCompressor).csv"  # Key (path) in the S3 bucket

# URL to download the ZIP file
url = "https://archive.ics.uci.edu/static/public/791/metropt+3+dataset.zip"

# Local paths
raw_data_dir = "/workspaces/Automated-Predictive-Maintenance/data/raw/"
os.makedirs(raw_data_dir, exist_ok=True)  # Ensure the directory exists
zip_file_path = os.path.join(raw_data_dir, "metropt3_dataset.zip")

# Step 1: Download the ZIP file
try:
    print(f"Downloading dataset from {url}...")
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    with open(zip_file_path, "wb") as f:
        f.write(response.content)
    print(f"Dataset downloaded and saved to: {zip_file_path}")
except Exception as e:
    print(f"Failed to download the dataset: {e}")
    exit()

# Step 2: Extract the ZIP file
try:
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(raw_data_dir)
    print(f"Dataset extracted to: {raw_data_dir}")
except Exception as e:
    print(f"Failed to extract the dataset: {e}")
    exit()

# Step 3: Load the CSV file into a pandas DataFrame
# Assuming the CSV file has the name 'MetroPT3(AirCompressor).csv' inside the ZIP
csv_file_name = "MetroPT3(AirCompressor).csv"
csv_file_path = os.path.join(raw_data_dir, csv_file_name)

try:
    data = pd.read_csv(csv_file_path)
    print(f"Loaded dataset into DataFrame with shape: {data.shape}")
except Exception as e:
    print(f"Failed to load the CSV file: {e}")
    exit()

# Step 4: Save the DataFrame to the raw data directory
try:
    raw_file_path = os.path.join(raw_data_dir, csv_file_name)
    data.to_csv(raw_file_path, index=False)
    print(f"Saved updated dataset to: {raw_file_path}")
except Exception as e:
    print(f"Failed to save the dataset locally: {e}")

# Step 5: Upload dataset to S3
try:
    s3.upload_file(raw_file_path, bucket_name, s3_key)  # Upload the file to S3
    print(f"Uploaded {csv_file_name} to s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"Failed to upload file to S3: {e}")
