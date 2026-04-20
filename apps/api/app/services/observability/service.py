from __future__ import annotations

from statistics import mean

from sqlalchemy.orm import Session

from app.models.entities import EvalRun, RetrievalRun


class ObservabilityService:
    def query_summary(self, db: Session) -> dict:
        retrieval_runs = list(db.query(RetrievalRun).all())
        eval_runs = list(db.query(EvalRun).all())
        latencies = [
            float(run.timings_json.get("answer", 0.0)) + float(run.timings_json.get("retrieve", 0.0))
            for run in retrieval_runs
            if run.timings_json
        ]
        return {
            "retrieval_runs": len(retrieval_runs),
            "eval_runs": len(eval_runs),
            "avg_response_ms": round(mean(latencies), 2) if latencies else 0.0,
            "latest_eval_status": eval_runs[0].status if eval_runs else "not_run",
        }

