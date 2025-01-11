import os
from alerts import log_alert

def test_log_alert():
    """
    Test if the log_alert function successfully writes alerts to a file.
    """
    # Path to the alerts file
    alerts_file_path = "/workspaces/Automated-Predictive-Maintenance/alerts/alerts.txt"

    # Log a sample alert
    log_alert("Test alert message", file_path=alerts_file_path)

    # Assert file exists
    assert os.path.exists(alerts_file_path), f"Alerts file not found at {alerts_file_path}"

    # Assert file contains the logged message
    with open(alerts_file_path, "r") as f:
        content = f.read()
    assert "Test alert message" in content, "Alert message not found in alerts file"
