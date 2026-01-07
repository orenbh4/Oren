from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_crash_without_env():
    r = client.get("/crash")
    assert r.status_code == 500
    assert r.json()["detail"] == "Missing REQUIRED_ENV"
