from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import httpx
import redis
from opensearchpy import OpenSearch
from qdrant_client import QdrantClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config.settings import Settings
from app.models.entities import ProviderState
from app.repositories.runs import RunRepository
from app.services.graph.service import GraphService
from app.services.reranking.service import RerankerService


@dataclass(slots=True)
class ProviderStatus:
    name: str
    kind: str
    status: str
    latency_ms: float | None
    details: dict[str, Any]


class ProviderHealthService:
    def __init__(
        self,
        settings: Settings,
        graph_service: GraphService,
        reranker: RerankerService,
    ) -> None:
        self.settings = settings
        self.graph_service = graph_service
        self.reranker = reranker

    def check_all(self, db: Session) -> list[ProviderState]:
        repo = RunRepository(db)
        states = [
            self._database(db),
            self._redis(),
            self._qdrant(),
            self._opensearch(),
            self._neo4j(),
            self._generator(),
            self._reranker(),
        ]
        persisted: list[ProviderState] = []
        for status in states:
            state = ProviderState(
                name=status.name,
                kind=status.kind,
                status=status.status,
                latency_ms=status.latency_ms,
                details_json=status.details,
                checked_at=datetime.now(timezone.utc),
            )
            repo.upsert_provider_state(state)
            persisted.append(state)
        db.commit()
        return persisted

    def _timed(self, name: str, kind: str, fn) -> ProviderStatus:
        started = time.perf_counter()
        try:
            details = fn()
            return ProviderStatus(
                name=name,
                kind=kind,
                status="healthy",
                latency_ms=(time.perf_counter() - started) * 1000,
                details=details,
            )
        except Exception as exc:  # pragma: no cover - network
            return ProviderStatus(
                name=name,
                kind=kind,
                status="degraded",
                latency_ms=(time.perf_counter() - started) * 1000,
                details={"reason": str(exc)},
            )

    def _database(self, db: Session) -> ProviderStatus:
        return self._timed("postgres", "database", lambda: {"ok": db.execute(text("SELECT 1")).scalar() == 1})

    def _redis(self) -> ProviderStatus:
        return self._timed(
            "redis",
            "cache",
            lambda: {"ok": redis.Redis.from_url(self.settings.redis_url).ping()},
        )

    def _qdrant(self) -> ProviderStatus:
        return self._timed(
            "qdrant",
            "vector_store",
            lambda: {"collections": len(QdrantClient(url=self.settings.qdrant_url).get_collections().collections)},
        )

    def _opensearch(self) -> ProviderStatus:
        def ping() -> dict[str, Any]:
            auth = None
            if self.settings.opensearch_username:
                auth = (self.settings.opensearch_username, self.settings.opensearch_password)
            client = OpenSearch(hosts=[self.settings.opensearch_url], http_auth=auth)
            return client.info()

        return self._timed("opensearch", "lexical_store", ping)

    def _neo4j(self) -> ProviderStatus:
        status, details = self.graph_service.ping()
        return ProviderStatus(name="neo4j", kind="graph", status=status, latency_ms=None, details=details)

    def _generator(self) -> ProviderStatus:
        provider = self.settings.generator_provider
        if provider == "extractive" or self.settings.disable_generation:
            return ProviderStatus(
                name="extractive",
                kind="generator",
                status="healthy",
                latency_ms=0.0,
                details={"mode": "deterministic extractive fallback"},
            )
        if provider == "openai":
            return self._timed(
                "openai-compatible",
                "generator",
                lambda: httpx.get(f"{self.settings.openai_base_url}/models", headers={"Authorization": f"Bearer {self.settings.openai_api_key}"}, timeout=4.0).json(),
            )
        if provider == "ollama":
            return self._timed(
                "ollama",
                "generator",
                lambda: httpx.get(f"{self.settings.ollama_base_url}/api/tags", timeout=4.0).json(),
            )
        return ProviderStatus(name=provider, kind="generator", status="degraded", latency_ms=None, details={"reason": "unsupported provider"})

    def _reranker(self) -> ProviderStatus:
        return ProviderStatus(
            name="cross-encoder",
            kind="reranker",
            status="healthy" if self.reranker.available() else "degraded",
            latency_ms=None,
            details={"available": self.reranker.available(), "fallback": "fusion-score ordering"},
        )

