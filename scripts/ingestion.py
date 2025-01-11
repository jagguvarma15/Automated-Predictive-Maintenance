import boto3
import pandas as pd
import os
import requests
import zipfile

# AWS S3 configuration
s3 = boto3.client("s3")
bucket_name = "raw-data-apm"
s3_key = "MetroPT3(AirCompressor).csv"  # Key (path) in the S3 bucket

# URL to download the ZIP file
url = "https://archive.ics.uci.edu/static/public/791/metropt+3+dataset.zip"

# Local paths
raw_data_dir = "./data/raw/"
os.makedirs(raw_data_dir, exist_ok=True)  # Ensure the directory exists
zip_file_path = os.path.join(raw_data_dir, "metropt3_dataset.zip")

# Step 1: Download the ZIP file
try:
    print(f"Downloading dataset from {url}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # Raise an error for bad responses
    with open(zip_file_path, "wb") as file:
        file.write(response.content)
    print(f"Dataset downloaded and saved to: {zip_file_path}")
except requests.RequestException as e:
    print(f"Failed to download the dataset: {e}")
    exit(1)

# Step 2: Extract the ZIP file
try:
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(raw_data_dir)
    print(f"Dataset extracted to: {raw_data_dir}")
except zipfile.BadZipFile as e:
    print(f"Failed to extract the dataset: {e}")
    exit(1)

# Step 3: Load the CSV file into a pandas DataFrame
csv_file_name = "MetroPT3(AirCompressor).csv"
csv_file_path = os.path.join(raw_data_dir, csv_file_name)

try:
    data = pd.read_csv(csv_file_path)
    print(f"Loaded dataset into DataFrame with shape: {data.shape}")
except FileNotFoundError as e:
    print(f"Failed to load the CSV file: {e}")
    exit(1)
except pd.errors.ParserError as e:
    print(f"Error parsing the CSV file: {e}")
    exit(1)

# Step 4: Save the DataFrame to the raw data directory
try:
    raw_file_path = os.path.join(raw_data_dir, csv_file_name)
    data.to_csv(raw_file_path, index=False)
    print(f"Saved updated dataset to: {raw_file_path}")
except IOError as e:
    print(f"Failed to save the dataset locally: {e}")
    exit(1)

# Step 5: Upload dataset to S3
try:
    s3.upload_file(raw_file_path, bucket_name, s3_key)
    print(f"Uploaded {csv_file_name} to s3://{bucket_name}/{s3_key}")
except boto3.exceptions.S3UploadFailedError as e:
    print(f"Failed to upload file to S3: {e}")
    exit(1)
