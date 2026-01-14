import pandas as pd

class ReorderAgent:
    def __init__(
        self,
        safety_stock: int,
        lead_time_days: int = 7,
        holding_cost_per_unit: float = 0.5,
        stockout_cost_per_unit: float = 5.0
    ):
        self.safety_stock = safety_stock
        self.lead_time_days = lead_time_days
        self.holding_cost_per_unit = holding_cost_per_unit
        self.stockout_cost_per_unit = stockout_cost_per_unit

    def generate_orders(self, low_stock_df, forecast_df):
        orders = []

        if low_stock_df.empty or forecast_df.empty:
            return orders

        # Average forecasted daily demand
        avg_daily_demand = forecast_df["forecast"].mean()

        for _, row in low_stock_df.iterrows():
            sku = row["sku"]
            current_stock = row["current_stock"]

            # Demand during lead time
            demand_during_lead_time = avg_daily_demand * self.lead_time_days

            # ---------------------------
            # Cost-based calculations
            # ---------------------------
            shortage = max(demand_during_lead_time - current_stock, 0)
            excess_stock = max(current_stock - demand_during_lead_time, 0)

            stockout_cost = shortage * self.stockout_cost_per_unit
            holding_cost = excess_stock * self.holding_cost_per_unit

            # ---------------------------
            # Confidence score (NEW)
            # ---------------------------
            confidence = min(
                1.0,
                stockout_cost / (stockout_cost + holding_cost + 1e-6)
            )

            # Reorder quantity
            reorder_qty = max(
                int(demand_during_lead_time + self.safety_stock - current_stock),
                0
            )

            if reorder_qty > 0:
                # Default explanation
                explanation = (
                    f"Forecasted demand over next {self.lead_time_days} days is "
                    f"{round(demand_during_lead_time, 2)} units. "
                    f"Current stock is {current_stock} units."
                )

                # ---------------------------
                # Cost-aware decision logic
                # ---------------------------
                if stockout_cost > holding_cost:
                    explanation = (
                        f"Stockout cost ({round(stockout_cost, 2)}) exceeds holding cost "
                        f"({round(holding_cost, 2)}). "
                        f"Forecasted demand over next {self.lead_time_days} days is "
                        f"{round(demand_during_lead_time, 2)} units. "
                        f"Reorder recommended."
                    )

                orders.append({
                    "sku": sku,
                    "current_stock": current_stock,
                    "forecast_demand": round(demand_during_lead_time, 2),
                    "safety_stock": self.safety_stock,
                    "lead_time_days": self.lead_time_days,
                    "recommended_order_qty": reorder_qty,
                    "stockout_cost": round(stockout_cost, 2),
                    "holding_cost": round(holding_cost, 2),
                    "confidence": round(confidence * 100, 1),
                    "explanation": explanation
                })

        return orders
