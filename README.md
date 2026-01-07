AI-Driven DevOps Incident Automation

This project demonstrates an end-to-end AI-powered DevOps incident automation pipeline.
It automatically detects application crashes using Prometheus, triggers Alertmanager, performs AI-based Root Cause Analysis, and opens GitHub incidents — all visualized in Grafana.

🧠 Architecture Flow

Application crash occurs

/metrics exposes demo_app_crashes_total

Prometheus scrapes metrics

Alert rule fires in alerts.yml

Alertmanager sends webhook to FastAPI

AI Engine performs Root Cause Analysis

GitHub issue is automatically created

Grafana dashboards visualize the incident

🛠 Stack
Component	Purpose
FastAPI	Application + Alertmanager webhook receiver
Prometheus	Metrics scraping
Alertmanager	Alert routing
Grafana	Dashboards
Docker Compose	Infrastructure orchestration
GitHub REST API	Incident creation
AI Engine	Root Cause Analysis
GitHub Actions	CI pipeline
📂 Project Structure
ai-devops-automation/
│
├─ app/
│   ├─ main.py
│   ├─ test_main.py
│   ├─ requirements.txt
│   └─ Dockerfile
│
├─ ai-engine/
│   ├─ analyzer.py
│   └─ Dockerfile
│
├─ prometheus/
│   ├─ prometheus.yml
│   └─ alerts.yml
│
├─ alertmanager/
│   └─ alertmanager.yml
│
├─ .github/workflows/
│   └─ ci.yml
│
├─ docker-compose.yml
└─ README.md

🚀 Run Locally (FastAPI only)
cd app
pip install -r requirements.txt
uvicorn main:app --reload

🐳 Run Full Stack with Docker Compose
docker compose up -d --build

🌐 Service URLs
Service	URL
Demo App	http://localhost:8000

Metrics	http://localhost:8000/metrics

Prometheus	http://localhost:9090

Alertmanager	http://localhost:9093

Grafana	http://localhost:3000

GitHub Issues	https://github.com/orenbh4/Oren/issues

Grafana credentials:

user: admin
pass: admin

📊 Prometheus Metrics
Metric
demo_app_crashes_total
demo_app_issues_created_total
📈 Grafana Panels (PromQL)
Panel	Query
AI Crashes Total	demo_app_crashes_total
Crash Rate / Minute	rate(demo_app_crashes_total[1m]) * 60
Crashes in Last 5 Minutes	increase(demo_app_crashes_total[5m])
GitHub Issues Created	demo_app_issues_created_total
🚨 Alert Rules (alerts.yml)
- alert: DemoAppHighCrashRate
  expr: increase(demo_app_crashes_total[5m]) >= 1
  for: 5s
  labels:
    service: demo-app
    severity: page
  annotations:
    summary: High crash rate detected in demo-app

🔔 Alertmanager Webhook (alertmanager.yml)
route:
  receiver: demo-app-webhook

receivers:
- name: demo-app-webhook
  webhook_configs:
  - url: "http://demo-app:8000/alerts"
    send_resolved: true

💥 Trigger a Crash
curl http://localhost:8000/crash-ai


This will:

Increment crash counter

Fire Prometheus alert

Alertmanager sends webhook

AI Engine analyzes crash

GitHub issue is created automatically

🧪 Verify Alert Webhook Manually
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{}'
