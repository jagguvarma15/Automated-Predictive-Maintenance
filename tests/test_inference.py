import numpy as np
from inference import run_inference, load_model

def test_inference():
    """
    Test if the inference function produces valid predictions.
    """
    # Load the model
    model_path = "/workspaces/Automated-Predictive-Maintenance/models/xgboost_model.json"
    model = load_model(model_path)

    # Input data for testing
    input_data = {"pressure": 45.0, "temperature": 30.5, "motor_current": 7.2}

    # Run inference
    result = run_inference(input_data, model)

    # Assert valid prediction output
    assert "prediction" in result and "probability" in result, "Inference result is missing keys"
    assert result["prediction"] in [0, 1], "Invalid prediction value"
    assert 0 <= result["probability"] <= 1, "Probability is out of range"
