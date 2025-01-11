import argparse
import os
import pandas as pd
import xgboost as xgb


def train_xgboost(train_path, model_output_path):
    """
    Trains an XGBoost model using the provided training data and saves it to the specified path.

    Args:
        train_path (str): Path to the training data (local or S3).
        model_output_path (str): Path to save the trained model.
    """
    # Ensure output directory exists
    os.makedirs(model_output_path, exist_ok=True)

    # Load training data
    print(f"Loading training data from {train_path}")
    try:
        data = pd.read_parquet(train_path)
    except FileNotFoundError as e:
        print(f"Training data file not found: {e}")
        exit(1)
    except Exception as e:
        print(f"Failed to load training data: {e}")
        exit(1)

    # Split data into features (X) and target (y)
    try:
        X = data[["pressure", "temperature", "motor_current"]]
        y = data["air_intake"]
        print("Data successfully split into features and target.")
    except KeyError as e:
        print(f"Missing expected columns in training data: {e}")
        exit(1)

    # Train the model using XGBoost
    print("Training the XGBoost model...")
    dtrain = xgb.DMatrix(X, label=y)
    params = {
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "max_depth": 5,
        "eta": 0.1,
        "seed": 42,
    }
    try:
        model = xgb.train(params, dtrain, num_boost_round=100)
        print("Model training completed successfully.")
    except Exception as e:
        print(f"Failed to train the model: {e}")
        exit(1)

    # Save the trained model
    model_path = os.path.join(model_output_path, "xgboost_model.json")
    try:
        model.save_model(model_path)
        print(f"Model saved successfully at {model_path}")
    except Exception as e:
        print(f"Failed to save the model: {e}")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train",
        type=str,
        default=None,
        help="Path to training data (local or S3)",
    )
    parser.add_argument(
        "--model_output",
        type=str,
        default=None,
        help="Path to save trained model",
    )
    args = parser.parse_args()

    # Use defaults for local debugging
    train_path = args.train or "/workspaces/Automated-Predictive-Maintenance/data/processed/MetroPT3_cleaned.parquet"
    model_output_path = args.model_output or "/workspaces/Automated-Predictive-Maintenance/models/"

    # Train the model
    train_xgboost(train_path, model_output_path)
