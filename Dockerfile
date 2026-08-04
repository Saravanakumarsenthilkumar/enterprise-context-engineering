# Multi-stage Dockerfile for Enterprise Context Engineering Service
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim AS runner

WORKDIR /app

RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser appuser

COPY --from=builder /install /usr/local
COPY src /app/src

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
