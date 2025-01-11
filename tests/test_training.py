import os
import xgboost as xgb

def test_training():
    """
    Test if the model training script successfully creates and saves the model.
    """
    # Path to the trained model
    model_path = "/workspaces/Automated-Predictive-Maintenance/models/xgboost_model.json"

    # Assert model file exists
    assert os.path.exists(model_path), f"Trained model file not found at {model_path}"

    # Assert model file can be loaded
    try:
        model = xgb.Booster()
        model.load_model(model_path)
    except Exception as e:
        assert False, f"Failed to load model: {e}"
