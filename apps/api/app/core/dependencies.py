from __future__ import annotations

from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.settings import Settings, get_settings
from app.db.session import get_db
from app.services.chat.service import ChatService
from app.services.citations.service import CitationService
from app.services.evals.service import EvalService
from app.services.graph.service import GraphService
from app.services.ingestion.service import IngestionService
from app.services.observability.service import ObservabilityService
from app.services.policy.guardrails import GuardrailService
from app.services.providers.service import ProviderHealthService
from app.services.retrieval.pipeline import LocalRetrievalIndex
from app.services.reranking.service import RerankerService


class ServiceContainer:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.local_index = LocalRetrievalIndex()
        self.reranker = RerankerService()
        self.citations = CitationService()
        self.guardrails = GuardrailService()
        self.graph = GraphService(settings)
        self.providers = ProviderHealthService(settings, self.graph, self.reranker)
        self.observability = ObservabilityService()
        self.ingestion = IngestionService(settings, self.local_index, self.graph)

    def chat(self, db: Session) -> ChatService:
        return ChatService(db, self.local_index, self.reranker, self.citations, self.guardrails)

    def evals(self, db: Session) -> EvalService:
        return EvalService(self.settings, self.chat(db))


@lru_cache(maxsize=1)
def get_container() -> ServiceContainer:
    return ServiceContainer(get_settings())


def get_chat_service(
    db: Session = Depends(get_db),
    container: ServiceContainer = Depends(get_container),
) -> ChatService:
    return container.chat(db)


def get_eval_service(
    db: Session = Depends(get_db),
    container: ServiceContainer = Depends(get_container),
) -> EvalService:
    return container.evals(db)

