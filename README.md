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

