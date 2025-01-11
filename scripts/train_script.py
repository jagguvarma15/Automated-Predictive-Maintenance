import argparse
import pandas as pd
import xgboost as xgb
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=str, default=None, help="Path to training data (local or S3)")
    parser.add_argument("--model_output", type=str, default=None, help="Path to save trained model")
    args = parser.parse_args()

    # Use defaults for local debugging
    train_path = args.train or "/workspaces/Automated-Predictive-Maintenance/data/processed/MetroPT3_cleaned.parquet"
    model_output_path = args.model_output or "/workspaces/Automated-Predictive-Maintenance/models/"

    # Ensure output directory exists
    os.makedirs(model_output_path, exist_ok=True)

    # Load training data
    print(f"Loading training data from {train_path}")
    data = pd.read_parquet(train_path)

    # Split data into features (X) and target (y)
    X = data[["pressure", "temperature", "motor_current"]]
    y = data["air_intake"]

    # Train the model using XGBoost
    dtrain = xgb.DMatrix(X, label=y)
    params = {
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "max_depth": 5,
        "eta": 0.1,
        "seed": 42
    }
    model = xgb.train(params, dtrain, num_boost_round=100)

    # Save the trained model
    model_path = os.path.join(model_output_path, "xgboost_model.json")
    model.save_model(model_path)
    print(f"Model training complete. Model saved at {model_path}")
