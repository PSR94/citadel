from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_eval_service
from app.db.session import get_db
from app.repositories.runs import RunRepository
from app.schemas.evals import EvalRunDetail, EvalRunRequest, EvalRunSummary
from app.services.evals.service import EvalService

router = APIRouter(prefix="/api/v1/evals", tags=["evals"])


@router.get("", response_model=list[EvalRunSummary])
def list_evals(db: Session = Depends(get_db)) -> list[EvalRunSummary]:
    return [
        EvalRunSummary(
            id=run.id,
            profile=run.profile,
            status=run.status,
            metrics=run.metrics_json,
            created_at=run.created_at,
            completed_at=run.completed_at,
        )
        for run in RunRepository(db).list_eval_runs()
    ]


@router.post("/run", response_model=EvalRunDetail)
def run_eval(
    request: EvalRunRequest,
    db: Session = Depends(get_db),
    service: EvalService = Depends(get_eval_service),
) -> EvalRunDetail:
    run = service.run(db, request.profile)
    return EvalRunDetail(
        id=run.id,
        profile=run.profile,
        status=run.status,
        metrics=run.metrics_json,
        details=run.details_json,
        created_at=run.created_at,
        completed_at=run.completed_at,
    )


@router.get("/{eval_id}", response_model=EvalRunDetail)
def get_eval(eval_id: str, db: Session = Depends(get_db)) -> EvalRunDetail:
    run = RunRepository(db).get_eval_run(eval_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Eval {eval_id} not found")
    return EvalRunDetail(
        id=run.id,
        profile=run.profile,
        status=run.status,
        metrics=run.metrics_json,
        details=run.details_json,
        created_at=run.created_at,
        completed_at=run.completed_at,
    )

