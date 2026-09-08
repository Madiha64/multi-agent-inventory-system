## AI-Powered Multi-Agent Inventory Intelligence System

An **AI-powered multi-agent inventory management system** that monitors inventory, analyzes demand, detects anomalies, evaluates stock risk, recommends reorder actions, and generates intelligent alerts.

The system combines **multiple specialized AI agents**, a **FastAPI backend**, an interactive **inventory dashboard**, and **AWS EC2 deployment** to provide automated inventory decision support.

---

##  Project Overview

Traditional inventory systems often rely on fixed thresholds and manual monitoring.

This project uses a **multi-agent architecture** where each agent performs a specialized task and contributes to the overall inventory intelligence workflow.

### Main Capabilities

-  Inventory monitoring
-  Demand forecasting
-  Anomaly detection
-  Inventory risk analysis
-  Reorder recommendations
-  Automated alerts
-  Alert history tracking
-  SKU retry and suggestion logic
-  API key authentication
-  REST API using FastAPI
-  AWS EC2 deployment
-  Nginx reverse proxy
-  Systemd service for automatic API startup

---

##  Multi-Agent Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Inventory Dashboard │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API     │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
     ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
     │ Inventory      │   │ Demand         │   │ Anomaly        │
     │ Monitor Agent  │   │ Forecast Agent │   │ Detection Agent│
     └───────┬────────┘   └───────┬────────┘   └───────┬────────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │ Risk Analysis /    │
                       │ Decision Layer     │
                       └─────────┬──────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
             ┌────────────┐ ┌───────────┐ ┌──────────────┐
             │ Reorder    │ │ Alert     │ │ Alert History│
             │ Agent      │ │ Agent     │ │ Agent        │
             └────────────┘ └───────────┘ └──────────────┘
```
---

## AI Agents
### 1. 📦 Inventory Monitor Agent

Monitors inventory levels for individual SKUs and provides current stock-related information.

### Responsibilities:

Monitor stock levels
Analyze inventory status
Identify potential stock problems
Provide SKU-level inventory information

---
## 2. 📈 Demand Forecast Agent

Analyzes historical inventory and sales information to estimate future demand.

### Responsibilities:

Analyze historical sales
Generate demand forecasts
Support inventory planning
Help determine future stock requirements

---

## Anomaly Detection Agent

Identifies unusual patterns in inventory and sales behavior.

### Responsibilities:

Detect unusual inventory behavior
Identify abnormal sales patterns
Support early detection of potential inventory problems

---

## 4. Risk Analysis Agent

Evaluates inventory conditions and determines the overall inventory risk.

The system categorizes inventory risk into:

🟢 LOW
🟡 MEDIUM
🔴 HIGH

The risk analysis considers inventory conditions and reorder thresholds to provide an understandable explanation.

---

## 5. Reorder Agent

Provides reorder recommendations based on inventory conditions.

### Responsibilities:

Identify products requiring replenishment
Recommend reorder actions
Support inventory decision-making

---

## 6. 🔔 Alert Agent

Generates alerts when inventory conditions require attention.

### Responsibilities:

Generate inventory alerts
Prevent unnecessary duplicate alerts
Notify about important inventory conditions

---

## 7. 📋 Alert History Agent

Maintains historical information about generated inventory alerts.

### Responsibilities:

1.Track previous alerts
2.Maintain alert history
3.Support monitoring and analysis of inventory events

---

## 🔄 Intelligent Retry & SKU Handling

The API includes robust SKU handling.

If a user provides an invalid SKU, the API:

### Normalizes the SKU input.
** Checks whether the SKU exists.
** Returns the available SKUs.
** Provides a retry indication.
** Allows the user/system to retry using a valid SKU.

SKU matching is case-insensitive.

---

## 🔐 API Security

The FastAPI backend uses API key authentication to protect the inventory endpoints.

## 🚨 Inventory Risk API

**Endpoint:**

```http
GET /risk/{sku}
```

### Example

```http
GET /risk/item_a?reorder_threshold=20
```

### Response

```json
{
  "sku": "item_a",
  "risk_level": "LOW",
  "explanation": "Stock level is healthy"
}
```
---
  
## 🚀 API Endpoints

**Endpoint:**
### Health Check
```http
GET /
```
Used to verify that the API is running.

---

## Inventory Risk
```http
GET /risk/{sku}
```

### Example 
```http
GET /risk/item_a?reorder_threshold=20
```

### Response:
```json
{
  "sku": "item_a",
  "risk_level": "LOW",
  "explanation": "Stock level is healthy"
}

```
---

## Demand Forecast
```http
GET /forecast/{sku}
```
### Example:
```http

GET /forecast/item_a?window=7
```
The endpoint generates a demand forecast based on the selected forecasting window.

---

## 📸 Dashboard Screenshots
The project includes an interactive dashboard for visualizing inventory intelligence and AI-generated recommendations.

### Inventory Risk Analysis

![Risk Analysis](./screenshots/Risk_analysis.png)

### Demand Forecasting View

![Demand Forecast](./screenshots/risk_Demand_forecast.png)

### Reorder Recommendation

![Reorder Recommendation](./screenshots/Reorder_recommandation_view.png)

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| API Server | Uvicorn |
| AI Architecture | Multi-Agent System |
| Data Processing | Pandas |
| Machine Learning | Python ML Ecosystem |
| Dashboard | Streamlit |
| Deployment | AWS EC2 |
| Reverse Proxy | Nginx |
| Process Management | Systemd |
| Authentication | API Key |
| Version Control | Git & GitHub |

---

## AWS Deployment

The FastAPI backend was deployed on AWS EC2.

### Deployment Architecture
```text
                     Internet
                         │
                         ▼
                ┌────────────────┐
                │    AWS EC2     │
                │                │
                │    Nginx       │
                │      │         │
                │      ▼         │
                │   Uvicorn      │
                │      │         │
                │      ▼         │
                │   FastAPI      │
                │      │         │
                │      ▼         │
                │ Multi-Agent    │
                │   System       │
                └────────────────┘

```

---
## 🌐 Nginx Reverse Proxy

Nginx is configured as a reverse proxy in front of the FastAPI application.
```text
Client
   │
   ▼
Nginx :80
   │
   ▼
Uvicorn :8000
   │
   ▼
FastAPI
   │
   ▼
Multi-Agent Inventory System

```

---

## 🎯 Key Outcomes
### Multi-Agent Decision Support

Developed a modular AI architecture where specialized agents perform different inventory intelligence tasks.

 ### Automated Inventory Risk Analysis

Implemented SKU-level risk evaluation with interpretable risk levels and explanations.

###  Demand-Aware Inventory Planning

Integrated demand forecasting to support better inventory decisions.

###  Automated Reorder Recommendations

Created an agent-based mechanism for identifying products that may require replenishment.

### Intelligent Alerting

Implemented automated alerts with duplicate-prevention logic.

### Robust API

Added case-insensitive SKU handling, invalid-SKU responses, available SKU suggestions, and retry support.

### Secure API Access

Implemented API key authentication for protected FastAPI endpoints.

### Cloud Deployment

Successfully deployed the FastAPI application on AWS EC2 using:

EC2 + Nginx + Uvicorn + Systemd

---
## Future Improvements

Potential future improvements include:

* LLM-based reasoning agent
* Advanced inventory optimization
* More sophisticated forecasting models
* Reinforcement learning for reorder decisions
* Mobile-friendly dashboard
* HTTPS/SSL deployment
☁️ AWS Secrets Manager integration
📈 Real-time inventory streaming
🗄️ Production database integration
🔔 Email/SMS notification integration
📊 Advanced analytics and reporting

---
## Why Multi-Agent AI?

A single model can perform multiple tasks, but a multi-agent architecture provides a more modular and maintainable approach.

Each agent has a clearly defined responsibility:
```text
Monitor
   ↓
Forecast
   ↓
Detect Anomaly
   ↓
Analyze Risk
   ↓
Recommend Reorder
   ↓
Generate Alert
   ↓
Store Alert History

```
This makes the system easier to extend, debug, and integrate with additional AI capabilities.

---

## Project Highlights
1. Multi-Agent AI Architecture
2. FastAPI REST API
3. Demand Forecasting
4. Anomaly Detection
5. Inventory Risk Analysis
6. Automated Reorder Recommendations
7. Intelligent Alerting
8. SKU Validation & Retry Logic
9. API Key Authentication
10. Streamlit Dashboard
11. AWS EC2 Deployment
12. Nginx Reverse Proxy
13. Uvicorn
14. Systemd Service
15. GitHub Version Control

---
## Author

### Madiha

AI / Machine Learning Developer

Interested in:

Generative AI
Multi-Agent AI Systems
Computer Vision
Large Language Models
RAG Systems
Intelligent Automation
AI-powered Applications

---

