from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.core.dependencies import ServiceContainer, get_container
from app.db.session import get_db
from app.repositories.runs import RunRepository
from app.schemas.providers import ProviderStateView, PublicConfig

router = APIRouter(tags=["providers"])


@router.get("/api/v1/providers", response_model=list[ProviderStateView])
def providers(
    db: Session = Depends(get_db),
    container: ServiceContainer = Depends(get_container),
) -> list[ProviderStateView]:
    if not RunRepository(db).list_provider_states():
        container.providers.check_all(db)
    return [
        ProviderStateView(
            name=state.name,
            kind=state.kind,
            status=state.status,
            latency_ms=state.latency_ms,
            details=state.details_json,
            checked_at=state.checked_at,
        )
        for state in RunRepository(db).list_provider_states()
    ]


@router.get("/api/v1/config/public", response_model=PublicConfig)
def public_config() -> PublicConfig:
    settings = get_settings()
    return PublicConfig(
        app_name=settings.public_app_name,
        domain=settings.public_domain,
        retrieval={
            "top_k": settings.query_top_k,
            "graph_hops": settings.graph_hops,
            "context_max_chunks": settings.context_max_chunks,
            "storage_mode": settings.storage_mode,
        },
        generation={
            "provider": settings.generator_provider,
            "extractive_fallback": settings.allow_extractive_fallback,
        },
        governance={
            "rbac_ready": True,
            "audit_logging": True,
            "citation_enforcement": True,
        },
    )

