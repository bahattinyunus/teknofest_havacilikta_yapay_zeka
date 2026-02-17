import csv
import time
import json
from datetime import datetime
import os

class TelemetryLogger:
    def __init__(self, log_dir="data/logs"):
        """
        Initialize the TelemetryLogger.
        
        Args:
            log_dir (str): Directory to save log files.
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_filename = os.path.join(log_dir, f"flight_log_{timestamp}.csv")
        self.json_filename = os.path.join(log_dir, f"flight_log_{timestamp}.json")
        
        self.headers = ["timestamp", "roll", "pitch", "yaw", "altitude", "battery", "mode", "detections"]
        self._init_csv()

    def _init_csv(self):
        with open(self.csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)

    def log(self, state, detections=None):
        """
        Log current state and detections.
        
        Args:
            state (dict): Flight state dictionary.
            detections (list): List of detected objects.
        """
        timestamp = time.time()
        
        # Prepare row for CSV
        row = [
            timestamp,
            state.get("roll", 0),
            state.get("pitch", 0),
            state.get("yaw", 0),
            state.get("altitude", 0),
            state.get("battery", 0),
            state.get("mode", "UNKNOWN"),
            len(detections) if detections else 0
        ]
        
        with open(self.csv_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
            
        # Optional: Log full JSON for debug
        log_entry = {
            "timestamp": timestamp,
            "state": state,
            "detections": detections
        }
        
        with open(self.json_filename, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    logger = TelemetryLogger()
    logger.log({"roll": 0.1, "pitch": -0.2, "yaw": 90.0, "altitude": 10.5, "mode": "TEST"})
    print(f"Logged to {logger.csv_filename}")
