FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn "openai>=1.0.0" pydantic requests

COPY analyzer.py .

EXPOSE 9000

CMD ["uvicorn", "analyzer:app", "--host", "0.0.0.0", "--port", "9000"]
