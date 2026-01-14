import pandas as pd
import numpy as np

class AnomalyDetectionAgent:
    """
    Detects anomalies in sales demand using statistical thresholds
    """

    def __init__(self, window: int = 7, z_threshold: float = 2.5):
        self.window = window
        self.z_threshold = z_threshold

    def detect(self, df: pd.DataFrame):
        """
        Expects df with columns: ['date', 'sales']
        Returns df with anomaly flags
        """

        df = df.sort_values("date").copy()

        # Rolling statistics
        df["rolling_mean"] = df["sales"].rolling(self.window).mean()
        df["rolling_std"] = df["sales"].rolling(self.window).std()

        # Z-score
        df["z_score"] = (
            (df["sales"] - df["rolling_mean"]) /
            (df["rolling_std"] + 1e-6)
        )

        # Anomaly flag
        df["is_anomaly"] = df["z_score"].abs() > self.z_threshold

        return df
