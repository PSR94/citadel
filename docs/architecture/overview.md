# Architecture Overview

CITADEL separates runtime concerns into three layers:

1. Product interface in `apps/web`
2. Retrieval and governance API in `apps/api`
3. Infrastructure adapters and seeded datasets under `infra/` and `datasets/`

The backend uses SQLAlchemy-backed relational persistence for documents, chunks, runs, eval history, provider health, and audit events. Retrieval uses a deterministic local index for tests and degraded mode, while the architecture leaves clear seams for OpenSearch, Qdrant, and Neo4j-backed service mode.

The product shell treats citations, retrieval traces, provider posture, and evaluation outcomes as operator-visible surfaces rather than admin-only plumbing.

