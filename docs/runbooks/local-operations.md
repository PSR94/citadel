# Local Operations

## First run

1. Copy `.env.example` to `.env`
2. Run `./scripts/bootstrap/bootstrap.sh`
3. Run `docker compose up --build`
4. Open `http://localhost:3000`

## Useful API operations

- `POST /api/v1/ingest/reindex`
- `POST /api/v1/chat/query/debug`
- `POST /api/v1/evals/run`
- `GET /health/dependencies`

## Failure handling

- If OpenSearch, Qdrant, or Neo4j are unavailable, CITADEL still serves local retrieval traces.
- If the generator is unavailable, answers remain evidence-first and citation-bound.
- If eval thresholds fail, CI should block merges until the regression is understood.

