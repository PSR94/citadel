from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.runs import RunRepository

router = APIRouter(prefix="/api/v1/retrieval", tags=["retrieval"])


@router.get("/runs/{run_id}")
def get_retrieval_run(run_id: str, db: Session = Depends(get_db)) -> dict:
    run = RunRepository(db).get_retrieval_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Retrieval run {run_id} not found")
    return {
        "id": run.id,
        "query": run.query,
        "status": run.status,
        "request": run.request_json,
        "response": run.response_json,
        "timings": run.timings_json,
        "provider": run.provider_json,
        "created_at": run.created_at,
    }

