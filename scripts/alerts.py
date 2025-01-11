import os
from datetime import datetime

# Define a function to log alerts
def log_alert(message, file_path="/workspaces/Automated-Predictive-Maintenance/alerts/alerts.txt"):
    """
    Logs an alert to a file with a timestamp.

    Args:
        message (str): The alert message to log.
        file_path (str): Path to the file where the alert will be logged.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Create the log message with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"

    # Append the log to the file
    with open(file_path, "a") as file:
        file.write(log_message)
    print(f"Alert logged: {log_message.strip()}")
