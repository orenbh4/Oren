import os
import time
import traceback
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI(title="AI DevOps Automation Demo", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello")
def hello():
    return {"message": "hello from demo app"}


@app.get("/crash")
def crash():
    required = os.getenv("REQUIRED_ENV")
    if not required:
        raise HTTPException(status_code=500, detail="Missing REQUIRED_ENV")
    return {"ok": True, "required": required}


@app.get("/slow")
def slow(seconds: int = 2):
    time.sleep(max(0, min(seconds, 10)))
    return {"slept": seconds}


def create_github_issue(title: str, body: str):
    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GITHUB_OWNER")
    repo = os.getenv("GITHUB_REPO")

    if not token or not owner or not repo:
        return None

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "ai-devops-automation-demo",
    }

    payload = {"title": title, "body": body}

    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


@app.get("/crash-ai")
def crash_ai():
    try:
        required = os.getenv("REQUIRED_ENV")
        if not required:
            raise ValueError("Missing REQUIRED_ENV")

        return {"ok": True, "required": required}

    except Exception as e:
        log_text = traceback.format_exc()

        # Ask AI engine
        try:
            r = requests.post(
                os.getenv("AI_ENGINE_URL", "http://ai-engine:9000/analyze"),
                json={"service": "demo-app", "log": log_text},
                timeout=180,
            )
            r.raise_for_status()
            ai = r.json()
        except Exception as ai_err:
            raise HTTPException(
                status_code=500,
                detail={"error": str(e), "ai_engine_error": str(ai_err)},
            )

        # Create GitHub issue
        issue_url = None
        issue_error = None

        title = f"[demo-app] Crash: {str(e)}"
        body = (
            "## Error\n"
            f"```\n{str(e)}\n```\n\n"
            "## AI Engine\n"
            f"- engine: {ai.get('engine')}\n\n"
            "## AI Analysis\n"
            f"{ai.get('analysis')}\n\n"
            "## Stack Trace\n"
            f"```python\n{log_text}\n```\n"
        )

        try:
            issue = create_github_issue(title, body)
            if issue and isinstance(issue, dict):
                issue_url = issue.get("html_url")
        except Exception as ex:
            issue_error = str(ex)

        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "ai_engine": ai.get("engine"),
                "analysis": ai.get("analysis"),
                "issue_url": issue_url,
                "issue_error": issue_error,
            },
        )
