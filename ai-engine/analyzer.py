import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Optional OpenAI cloud support
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

app = FastAPI(title="AI Log Analyzer", version="0.3.0")

class LogRequest(BaseModel):
    service: str
    log: str


def analyze_with_ollama(prompt: str) -> str:
    """
    Calls local Ollama LLM running on the Windows host.
    """
    try:
        r = requests.post(
            "http://host.docker.internal:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=120
        )
        r.raise_for_status()
        return r.json()["response"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")


def analyze_with_openai(prompt: str) -> str:
    """
    Uses OpenAI cloud if OPENAI_API_KEY exists.
    """
    if not OpenAI:
        raise RuntimeError("OpenAI SDK not installed")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    client = OpenAI(api_key=api_key)

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
    )

    return resp.choices[0].message.content


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_log(req: LogRequest):
    prompt = (
        "You are a senior DevOps / SRE engineer.\n"
        "Analyze the following error log and respond with:\n"
        "1) Root cause\n"
        "2) Suggested fix\n"
        "3) Immediate mitigation\n\n"
        f"Service: {req.service}\n"
        f"Log:\n{req.log}\n"
    )

    # Try OpenAI first (if key exists), otherwise fallback to Ollama
    try:
        if os.getenv("OPENAI_API_KEY") and OpenAI:
            return {"engine": "openai", "analysis": analyze_with_openai(prompt)}
    except Exception:
        pass

    # Fallback to local Ollama
    return {"engine": "ollama", "analysis": analyze_with_ollama(prompt)}
