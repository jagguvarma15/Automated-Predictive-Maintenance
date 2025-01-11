import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def train_and_evaluate(data_path, model_output_path):
    """
    Train and evaluate an XGBoost model using the provided dataset.

    Args:
        data_path (str): Path to the processed dataset.
        model_output_path (str): Path to save the trained model.
    """
    try:
        # Load the processed data
        print(f"Loading processed data from: {data_path}")
        data = pd.read_parquet(data_path)
    except FileNotFoundError as e:
        print(f"Data file not found: {e}")
        exit(1)
    except Exception as e:
        print(f"Failed to load the dataset: {e}")
        exit(1)

    # Split data into features (X) and target (y)
    try:
        X = data[["pressure", "temperature", "motor_current"]]
        y = data["air_intake"]
        print("Dataset successfully split into features and target.")
    except KeyError as e:
        print(f"Missing expected columns in the dataset: {e}")
        exit(1)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("Data split into training and testing sets.")

    # Convert data to DMatrix for XGBoost
    dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=["pressure", "temperature", "motor_current"])
    dtest = xgb.DMatrix(X_test, label=y_test, feature_names=["pressure", "temperature", "motor_current"])

    # Define model parameters
    params = {
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "max_depth": 5,
        "eta": 0.1,
        "seed": 42,
    }

    # Train the model
    print("Training the XGBoost model...")
    try:
        model = xgb.train(params, dtrain, num_boost_round=100)
        print("Model training completed successfully.")
    except Exception as e:
        print(f"Failed to train the model: {e}")
        exit(1)

    # Save the trained model locally
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    try:
        model.save_model(model_output_path)
        print(f"Model saved successfully to: {model_output_path}")
    except Exception as e:
        print(f"Failed to save the model: {e}")
        exit(1)

    # Evaluate the model
    print("Evaluating the model...")
    preds = model.predict(dtest)
    predictions = [1 if pred > 0.5 else 0 for pred in preds]

    try:
        print("Accuracy:", accuracy_score(y_test, predictions))
        print(classification_report(y_test, predictions))
    except Exception as e:
        print(f"Failed to evaluate the model: {e}")
        exit(1)


if __name__ == "__main__":
    # Define paths
    data_path = "/workspaces/Automated-Predictive-Maintenance/data/processed/MetroPT3_cleaned.parquet"
    model_output_path = "/workspaces/Automated-Predictive-Maintenance/models/xgboost_model.json"

    # Train and evaluate the model
    train_and_evaluate(data_path, model_output_path)
