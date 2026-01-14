import datetime
import os
import pandas as pd


class AlertHistoryAgent:
    def __init__(self, file_path="data/alert_history.csv"):
        self.file_path = file_path

        # Create file if it does not exist
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(
                columns=["timestamp", "sku", "risk_level", "explanation"]
            )
            df.to_csv(self.file_path, index=False)

    def log(self, sku: str, risk_level: str, explanation: str):
        """
        Save alert to CSV
        """
        new_row = {
            "timestamp": datetime.datetime.now().isoformat(),
            "sku": sku,
            "risk_level": risk_level,
            "explanation": explanation
        }

        df = pd.read_csv(self.file_path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.file_path, index=False)

    def get_history(self):
        """
        Read alert history
        """
        if not os.path.exists(self.file_path):
            return []

        df = pd.read_csv(self.file_path)
        return df.to_dict(orient="records")
