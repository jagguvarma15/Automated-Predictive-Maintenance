import os
import pandas as pd

def test_etl():
    """
    Test if the ETL script successfully processes raw data into the processed data format.
    """
    # Path to the processed data file
    processed_data_path = "/workspaces/Automated-Predictive-Maintenance/data/processed/MetroPT3_cleaned.parquet"

    # Assert file exists after ETL
    assert os.path.exists(processed_data_path), f"Processed data file not found at {processed_data_path}"

    # Assert file contains valid data
    data = pd.read_parquet(processed_data_path)
    assert not data.empty, "Processed data is empty"

    # Assert expected columns exist
    expected_columns = ["pressure", "temperature", "motor_current", "air_intake"]
    assert all(col in data.columns for col in expected_columns), "Missing expected columns in processed data"
