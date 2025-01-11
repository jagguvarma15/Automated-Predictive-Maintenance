import xgboost as xgb
import numpy as np
from alerts import log_alert

# Path to the trained model
model_path = "/workspaces/Automated-Predictive-Maintenance/models/xgboost_model.json"

# Load the trained model
model = xgb.Booster()
model.load_model(model_path)

# Define a function for inference
def run_inference(input_data):
    """
    Runs inference on the input data using the trained XGBoost model.
    
    Args:
        input_data (dict): A dictionary containing input features.
            Example: {"pressure": 45.0, "temperature": 30.5, "motor_current": 7.2}

    Returns:
        dict: A dictionary containing the prediction and probability.
    """
    # Convert input data to a NumPy array
    input_array = np.array([[input_data["pressure"], input_data["temperature"], input_data["motor_current"]]])
    # Convert to XGBoost DMatrix
    dinput = xgb.DMatrix(input_array, feature_names=["pressure", "temperature", "motor_current"])
    # Predict
    pred_prob = model.predict(dinput)[0]
    pred = 1 if pred_prob > 0.5 else 0
    return {"prediction": pred, "probability": pred_prob}

# Example input data
input_data = {"pressure": 45.0, "temperature": 30.5, "motor_current": 7.2}

# Run inference
result = run_inference(input_data)

# Output the result
print(f"Prediction: {result['prediction']} (Probability: {result['probability']:.2f})")

# Log alert if the prediction indicates a high failure probability
if result["prediction"] == 1:
    log_alert(f"High failure probability detected! Probability: {result['probability']:.2f}")
