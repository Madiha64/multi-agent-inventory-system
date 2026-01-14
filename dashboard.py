import streamlit as st
import pandas as pd
import requests

# -------------------------------------------------
# Agent imports (UI-side only)
# -------------------------------------------------
from agents.alert_agent import AlertAgent
from agents.alert_history_agent import AlertHistoryAgent
from agents.anomaly_detection_agent import AnomalyDetectionAgent
from agents.reorder_agent import ReorderAgent

# -------------------------------------------------
# API config
# -------------------------------------------------
API_BASE_URL = "http://127.0.0.1:8000"

# -------------------------------------------------
# Utility: API health check
# -------------------------------------------------
def check_api_health():
    try:
        r = requests.get(f"{API_BASE_URL}/", timeout=2)
        return r.status_code == 200
    except:
        return False

# -------------------------------------------------
# Initialize agents (ONCE)
# -------------------------------------------------
alert_agent = AlertAgent()
alert_history_agent = AlertHistoryAgent()

# -------------------------------------------------
# Streamlit config
# -------------------------------------------------
st.set_page_config(page_title="Inventory AI Dashboard", layout="wide")
st.title("📦 Inventory AI Dashboard")

# -------------------------------------------------
# 🔍 API health guard (IMPORTANT)
# -------------------------------------------------
if not check_api_health():
    st.error("🚨 FastAPI backend is not running. Please start it with:")
    st.code("uvicorn api.main:app --reload")
    st.stop()
else:
    st.success("✅ Connected to FastAPI backend")

# -------------------------------------------------
# Load data
# -------------------------------------------------
df = pd.read_csv("data/inventory_sales.csv")

df = df.rename(columns={
    "product": "sku",
    "inventory": "current_stock"
})

required_columns = ["date", "sku", "current_stock", "sales"]
for col in required_columns:
    if col not in df.columns:
        st.error(f"❌ Missing required column: {col}")
        st.write("Found columns:", df.columns.tolist())
        st.stop()

df["date"] = pd.to_datetime(df["date"])

# -------------------------------------------------
# Sidebar controls
# -------------------------------------------------
st.sidebar.header("Controls")

selected_sku = st.sidebar.selectbox(
    "Select SKU",
    sorted(df["sku"].unique())
)

st.sidebar.subheader("Agent Parameters")

reorder_threshold = st.sidebar.slider(
    "Reorder Threshold", 0, 100, 20, 5
)

safety_stock = st.sidebar.slider(
    "Safety Stock", 0, 50, 10, 5
)

lead_time_days = st.sidebar.slider(
    "Lead Time (days)", 1, 30, 7
)

# -------------------------------------------------
# Filter SKU data
# -------------------------------------------------
df_sku = df[df["sku"] == selected_sku]

# -------------------------------------------------
# 🔍 Anomaly Detection (local analytics)
# -------------------------------------------------
anomaly_agent = AnomalyDetectionAgent(window=7, z_threshold=2.5)
anomaly_df = anomaly_agent.detect(df_sku[["date", "sales"]])

num_anomalies = anomaly_df["is_anomaly"].sum()

if num_anomalies > 0:
    st.warning(f"⚠️ {num_anomalies} demand anomalies detected")
else:
    st.success("✅ No demand anomalies detected")

st.subheader("📊 Demand Anomaly Detection")
st.line_chart(
    anomaly_df.set_index("date")[["sales", "rolling_mean"]]
)

# -------------------------------------------------
# 🔌 Fetch Risk from FastAPI
# -------------------------------------------------
risk_response = requests.get(
    f"{API_BASE_URL}/risk/{selected_sku}",
    params={"reorder_threshold": reorder_threshold},
    timeout=5
)

if risk_response.status_code != 200:
    st.error("❌ Failed to fetch risk from API")
    st.stop()

risk_data = risk_response.json()
risk_label = risk_data["risk_level"]
risk_explanation = risk_data["explanation"]

# 🔍 DEBUG PANEL — RISK
with st.expander("🔍 API Debug – Risk Response"):
    st.json(risk_data)

# -------------------------------------------------
# 🚨 Alert Trigger + History
# -------------------------------------------------
if alert_agent.should_alert(selected_sku, risk_label):
    st.error(f"🚨 HIGH RISK ALERT for SKU `{selected_sku}`")

    alert_history_agent.log(
        sku=selected_sku,
        risk_level=risk_label,
        explanation=risk_explanation
    )

# -------------------------------------------------
# 🏷 Risk Badge
# -------------------------------------------------
st.markdown(f"## 🔍 Selected SKU: `{selected_sku}`")

if risk_label == "LOW":
    st.success(f"🟢 Risk Level: {risk_label}")
elif risk_label == "MEDIUM":
    st.warning(f"🟡 Risk Level: {risk_label}")
else:
    st.error(f"🔴 Risk Level: {risk_label}")

st.caption(f"Explanation: {risk_explanation}")

# -------------------------------------------------
# 🔌 Fetch Forecast from FastAPI
# -------------------------------------------------
forecast_response = requests.get(
    f"{API_BASE_URL}/forecast/{selected_sku}",
    params={"window": 7},
    timeout=5
)

if forecast_response.status_code != 200:
    st.error("❌ Failed to fetch forecast from API")
    st.stop()

forecast_data = forecast_response.json()
forecast_df = pd.DataFrame(forecast_data["forecast"])

# 🔍 DEBUG PANEL — FORECAST
with st.expander("🔍 API Debug – Forecast Response"):
    st.json(forecast_data)

st.subheader("📈 Demand Forecast")

if forecast_df.empty:
    st.info("Not enough data for forecast")
else:
    st.line_chart(
        forecast_df.set_index("date")["forecast"]
    )

# -------------------------------------------------
# 📦 Reorder Decision (forecast-aware)
# -------------------------------------------------
current_stock = int(df_sku["current_stock"].iloc[-1])
forecast_demand = forecast_df["forecast"].sum() if not forecast_df.empty else 0

reorder_agent = ReorderAgent(
    safety_stock=safety_stock,
    lead_time_days=lead_time_days
)

orders = reorder_agent.generate_orders(
    low_stock_df=pd.DataFrame([{
        "sku": selected_sku,
        "current_stock": current_stock,
        "forecast_demand": forecast_demand
    }]),
    forecast_df=forecast_df
)

st.subheader("📦 Reorder Recommendations")

if not orders:
    st.info("No reorder required")
else:
    st.dataframe(pd.DataFrame(orders), use_container_width=True)

# -------------------------------------------------
# 🕒 Alert History
# -------------------------------------------------
st.subheader("🕒 Alert History")

history = alert_history_agent.get_history()

if not history:
    st.info("No alerts logged yet.")
else:
    st.dataframe(pd.DataFrame(history), use_container_width=True)
