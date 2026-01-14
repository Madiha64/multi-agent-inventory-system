import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class DemandForecastAgent:
    def __init__(self, window: int = 3):
        self.window = window
        self.model = LinearRegression()

    def forecast(self, df: pd.DataFrame):
        forecasts = []

        for sku in df["sku"].unique():
            sku_df = df[df["sku"] == sku].sort_values("date").copy()

            # Feature engineering: lagged sales
            for i in range(1, self.window + 1):
                sku_df[f"lag_{i}"] = sku_df["sales"].shift(i)

            sku_df.dropna(inplace=True)

            if len(sku_df) < 3:
                continue

            X = sku_df[[f"lag_{i}" for i in range(1, self.window + 1)]]
            y = sku_df["sales"]

            self.model.fit(X, y)

            # Predict next value
            last_known = X.iloc[-1].values.reshape(1, -1)
            prediction = self.model.predict(last_known)[0]

            # Risk estimation (volatility)
            std_dev = sku_df["sales"].std()

            if std_dev > 8:
                risk = "HIGH"
            elif std_dev > 4:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            forecasts.append({
                "date": sku_df["date"].iloc[-1] + pd.Timedelta(days=1),
                "sku": sku,
                "forecast": max(prediction, 0),
                "risk_level": risk
            })

        return pd.DataFrame(forecasts)
