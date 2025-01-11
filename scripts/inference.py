import numpy as np
import xgboost as xgb
from alerts import log_alert


def load_model(model_path):
    """
    Loads a trained XGBoost model from the specified path.

    Args:
        model_path (str): Path to the trained model.

    Returns:
        xgb.Booster: Loaded XGBoost model.
    """
    try:
        model = xgb.Booster()
        model.load_model(model_path)
        print(f"Model loaded successfully from: {model_path}")
        return model
    except FileNotFoundError as e:
        print(f"Model file not found: {e}")
        exit(1)
    except Exception as e:
        print(f"Failed to load model: {e}")
        exit(1)


def run_inference(input_data, model):
    """
    Runs inference on the input data using the trained XGBoost model.

    Args:
        input_data (dict): A dictionary containing input features.
            Example: {"pressure": 45.0, "temperature": 30.5, "motor_current": 7.2}
        model (xgb.Booster): The trained XGBoost model.

    Returns:
        dict: A dictionary containing the prediction and probability.
    """
    try:
        # Convert input data to a NumPy array
        input_array = np.array([[input_data["pressure"], input_data["temperature"], input_data["motor_current"]]])
        # Convert to XGBoost DMatrix
        dinput = xgb.DMatrix(input_array, feature_names=["pressure", "temperature", "motor_current"])
        # Predict
        pred_prob = model.predict(dinput)[0]
        pred = 1 if pred_prob > 0.5 else 0
        return {"prediction": pred, "probability": pred_prob}
    except KeyError as e:
        print(f"Missing input feature: {e}")
        exit(1)
    except Exception as e:
        print(f"Failed to run inference: {e}")
        exit(1)


if __name__ == "__main__":
    # Path to the trained model
    model_path = "/workspaces/Automated-Predictive-Maintenance/models/xgboost_model.json"

    # Example input data
    input_data = {"pressure": 45.0, "temperature": 30.5, "motor_current": 7.2}

    # Load the model
    model = load_model(model_path)

    # Run inference
    result = run_inference(input_data, model)

    # Output the result
    print(f"Prediction: {result['prediction']} (Probability: {result['probability']:.2f})")

    # Log alert if the prediction indicates a high failure probability
    if result["prediction"] == 1:
        log_alert(f"High failure probability detected! Probability: {result['probability']:.2f}")
