from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.core.dependencies import ServiceContainer, get_container
from app.db.session import get_db
from app.schemas.ingestion import IngestionRunSummary

router = APIRouter(prefix="/api/v1/ingest", tags=["ingestion"])


@router.post("/reindex", response_model=IngestionRunSummary)
def reindex(
    db: Session = Depends(get_db),
    container: ServiceContainer = Depends(get_container),
) -> IngestionRunSummary:
    run = container.ingestion.ingest_directory(db, trigger="reindex")
    return IngestionRunSummary(
        id=run.id,
        trigger=run.trigger,
        status=run.status,
        processed_documents=run.processed_documents,
        processed_chunks=run.processed_chunks,
        error_count=run.error_count,
        summary=run.summary_json,
        created_at=run.created_at,
        completed_at=run.completed_at,
    )


@router.post("/upload", response_model=IngestionRunSummary)
async def upload_and_ingest(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    container: ServiceContainer = Depends(get_container),
) -> IngestionRunSummary:
    settings = get_settings()
    upload_dir = settings.dataset_dir.parent / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    target = upload_dir / file.filename
    target.write_bytes(await file.read())
    run = container.ingestion.ingest_directory(db, path=upload_dir, trigger="upload")
    return IngestionRunSummary(
        id=run.id,
        trigger=run.trigger,
        status=run.status,
        processed_documents=run.processed_documents,
        processed_chunks=run.processed_chunks,
        error_count=run.error_count,
        summary={**run.summary_json, "uploaded_file": str(Path(target).name)},
        created_at=run.created_at,
        completed_at=run.completed_at,
    )

