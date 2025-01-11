import os
import pandas as pd

def test_ingestion():
    """
    Test if the data ingestion script successfully downloads and saves the dataset.
    """
    # Path to the raw data file
    raw_data_path = "/workspaces/Automated-Predictive-Maintenance/data/raw/MetroPT3(AirCompressor).csv"

    # Assert file exists after ingestion
    assert os.path.exists(raw_data_path), f"Raw data file not found at {raw_data_path}"

    # Assert file contains valid data
    data = pd.read_csv(raw_data_path)
    assert not data.empty, "Ingested data is empty"
