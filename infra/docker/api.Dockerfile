FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY apps/api /workspace/apps/api
COPY datasets /workspace/datasets
COPY .env.example /workspace/.env.example
COPY README.md /workspace/README.md

RUN python -m pip install --upgrade pip && \
    cd /workspace/apps/api && \
    python -m pip install -e ".[dev]"

WORKDIR /workspace/apps/api

EXPOSE 8000

