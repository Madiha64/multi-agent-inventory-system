class InventoryMonitorAgent:
    def __init__(self, reorder_threshold=20):
        self.reorder_threshold = reorder_threshold

    def check_inventory(self, inventory_df):
        """
        Returns rows where stock is below reorder threshold
        """
        return inventory_df[
            inventory_df["current_stock"] < self.reorder_threshold
        ]

    def assess_risk(self, inventory_df):
        """
        Assess overall inventory risk for selected SKU
        """
        latest_row = inventory_df.sort_values("date").iloc[-1]
        current_stock = latest_row["current_stock"]

        if current_stock < self.reorder_threshold:
            return {
                "risk_level": "HIGH",
                "explanation": "Stock is below reorder threshold"
            }
        elif current_stock < self.reorder_threshold * 1.5:
            return {
                "risk_level": "MEDIUM",
                "explanation": "Stock is approaching reorder threshold"
            }
        else:
            return {
                "risk_level": "LOW",
                "explanation": "Stock level is healthy"
            }


