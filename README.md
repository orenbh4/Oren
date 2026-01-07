## 🔥 AI-Driven DevOps Incident Automation

This system detects application crashes in real-time using Prometheus,
automatically triggers Alertmanager, runs AI-powered Root Cause Analysis,
and opens GitHub incidents with diagnostic insights.

Stack:
- FastAPI
- Prometheus + Alertmanager
- Grafana
- Docker Compose
- GitHub API Automation
- AI Root Cause Analyzer


# AI DevOps Automation (Demo)

Stage 1: FastAPI app + Docker + GitHub Actions CI.

## Run locally
```bash
cd app
pip install -r requirements.txt
uvicorn main:app --reload


## Run locally with Docker Compose

### Start services
```bash
docker compose up --build

