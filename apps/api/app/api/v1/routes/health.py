from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.core.dependencies import ServiceContainer, get_container
from app.db.session import get_db
from app.models.entities import Document

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.public_app_name,
        "environment": settings.app_env,
        "checked_at": datetime.now(timezone.utc),
    }


@router.get("/dependencies")
def dependency_health(
    db: Session = Depends(get_db),
    container: ServiceContainer = Depends(get_container),
) -> list[dict]:
    states = container.providers.check_all(db)
    return [
        {
            "name": state.name,
            "kind": state.kind,
            "status": state.status,
            "latency_ms": state.latency_ms,
            "details": state.details_json,
            "checked_at": state.checked_at,
        }
        for state in states
    ]


@router.get("/readiness")
def readiness(
    db: Session = Depends(get_db),
    container: ServiceContainer = Depends(get_container),
) -> dict:
    document_count = db.query(Document).count()
    ready = document_count > 0 and container.local_index.ready()
    return {
        "status": "ready" if ready else "warming",
        "documents": document_count,
        "local_index_ready": container.local_index.ready(),
        "checked_at": datetime.now(timezone.utc),
    }

