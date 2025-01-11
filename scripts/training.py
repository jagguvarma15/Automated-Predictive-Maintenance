import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Path to processed data
data_path = "/workspaces/Automated-Predictive-Maintenance/data/processed/MetroPT3_cleaned.parquet"

# Load the processed data
data = pd.read_parquet(data_path)

# Split data into features (X) and target (y)
X = data[["pressure", "temperature", "motor_current"]]
y = data["air_intake"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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
model = xgb.train(params, dtrain, num_boost_round=100)

# Save the trained model locally
model.save_model("/workspaces/Automated-Predictive-Maintenance/models/xgboost_model.json")
print("Model training complete. Model saved to models/xgboost_model.json")

# Evaluate the model
preds = model.predict(dtest)
predictions = [1 if pred > 0.5 else 0 for pred in preds]
print("Accuracy:", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))
