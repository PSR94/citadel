from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import AuditEvent, EvalRun, IngestionRun, ProviderState, RetrievalRun


class RunRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add_ingestion_run(self, run: IngestionRun) -> None:
        self.db.add(run)

    def add_retrieval_run(self, run: RetrievalRun) -> None:
        self.db.add(run)

    def add_eval_run(self, run: EvalRun) -> None:
        self.db.add(run)

    def list_eval_runs(self) -> list[EvalRun]:
        stmt = select(EvalRun).order_by(EvalRun.created_at.desc())
        return list(self.db.scalars(stmt))

    def get_eval_run(self, eval_id: str) -> EvalRun | None:
        return self.db.get(EvalRun, eval_id)

    def get_retrieval_run(self, run_id: str) -> RetrievalRun | None:
        return self.db.get(RetrievalRun, run_id)

    def upsert_provider_state(self, state: ProviderState) -> None:
        current = self.db.get(ProviderState, state.name)
        if current:
            current.kind = state.kind
            current.status = state.status
            current.latency_ms = state.latency_ms
            current.details_json = state.details_json
            current.checked_at = state.checked_at
            return
        self.db.add(state)

    def list_provider_states(self) -> list[ProviderState]:
        stmt = select(ProviderState).order_by(ProviderState.kind.asc(), ProviderState.name.asc())
        return list(self.db.scalars(stmt))

    def add_audit_event(self, event: AuditEvent) -> None:
        self.db.add(event)

