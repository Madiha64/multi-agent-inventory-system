from fastapi import FastAPI
import pandas as pd

from agents.inventory_monitor_agent import InventoryMonitorAgent
from agents.alert_agent import AlertAgent
from agents.alert_history_agent import AlertHistoryAgent
from agents.demand_forecast_agent import DemandForecastAgent

app = FastAPI(
    title="Inventory AI Agent API",
    version="1.0"
)

DATA_PATH = "data/inventory_sales.csv"

alert_agent = AlertAgent()
alert_history_agent = AlertHistoryAgent()


# -------------------------
# Health Check
# -------------------------
@app.get("/")
def health_check():
    return {"status": "Inventory AI API running"}


# -------------------------
# Inventory Risk Endpoint
# -------------------------
@app.get("/risk/{sku}")
def get_inventory_risk(
    sku: str,
    reorder_threshold: int = 20
):
    df = pd.read_csv(DATA_PATH)

    df = df.rename(columns={
        "product": "sku",
        "inventory": "current_stock"
    })

    df_sku = df[df["sku"] == sku]

    if df_sku.empty:
        return {"error": "SKU not found"}

    monitor = InventoryMonitorAgent(
        reorder_threshold=reorder_threshold
    )

    risk = monitor.assess_risk(df_sku)

    if alert_agent.should_alert(sku, risk["risk_level"]):
        alert_history_agent.log(
            sku,
            risk["risk_level"],
            risk["explanation"]
        )

    return {
        "sku": sku,
        "risk_level": risk["risk_level"],
        "explanation": risk["explanation"]
    }


# -------------------------
# Demand Forecast Endpoint
# -------------------------
@app.get("/forecast/{sku}")
def get_demand_forecast(
    sku: str,
    window: int = 7
):
    df = pd.read_csv(DATA_PATH)

    df = df.rename(columns={
        "product": "sku",
        "inventory": "current_stock"
    })

    df_sku = df[df["sku"] == sku]

    if df_sku.empty:
        return {"error": "SKU not found"}

    # 🔒 SAFETY FIXES
    df_sku["date"] = pd.to_datetime(df_sku["date"])
    df_sku = df_sku.sort_values("date")
    df_sku = df_sku.dropna(subset=["sales"])

    if len(df_sku) < window:
        return {
            "error": "Not enough historical data",
            "available_records": len(df_sku),
            "requested_window": window
        }

    forecast_agent = DemandForecastAgent(window=window)
    forecast_df = forecast_agent.forecast(df_sku)

    return {
        "sku": sku,
        "window": window,
        "forecast": forecast_df.tail(5).to_dict(orient="records")
    }
