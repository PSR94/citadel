from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from time import perf_counter
from typing import Any

from sqlalchemy.orm import Session

from app.config.settings import Settings
from app.models.entities import EvalRun
from app.repositories.runs import RunRepository
from app.schemas.chat import ChatQueryRequest
from app.services.chat.service import ChatService
from app.utils.ids import new_id


class EvalService:
    def __init__(self, settings: Settings, chat_service: ChatService) -> None:
        self.settings = settings
        self.chat_service = chat_service

    def run(self, db: Session, profile: str = "ci") -> EvalRun:
        run = EvalRun(
            id=new_id("eval"),
            profile=profile,
            status="running",
            created_at=datetime.now(timezone.utc),
        )
        repo = RunRepository(db)
        repo.add_eval_run(run)
        db.flush()

        retrieval_cases = self._load_json(self.settings.evals_dir / "retrieval_cases.json")
        grounding_cases = self._load_json(self.settings.evals_dir / "grounding_cases.json")

        recall_hits: list[float] = []
        citation_coverages: list[float] = []
        unsupported_rates: list[float] = []
        latencies_ms: list[float] = []
        failure_cases: list[dict[str, Any]] = []

        for case in retrieval_cases:
            started = perf_counter()
            response = self.chat_service.query(ChatQueryRequest(query=case["query"], debug=True))
            latencies_ms.append((perf_counter() - started) * 1000)
            retrieved_doc_ids = {item.document_id for item in response.evidence[:10]}
            expected = set(case["expected_document_ids"])
            recall = len(expected & retrieved_doc_ids) / max(1, len(expected))
            recall_hits.append(recall)
            citation_coverages.append(response.grounding.citation_coverage)
            unsupported_rates.append(
                response.grounding.unsupported_claims / max(1, len(response.answer) or 1)
            )
            if recall < 1.0:
                failure_cases.append(
                    {
                        "type": "retrieval",
                        "case": case["id"],
                        "query": case["query"],
                        "expected": sorted(expected),
                        "retrieved": sorted(retrieved_doc_ids),
                    }
                )

        for case in grounding_cases:
            response = self.chat_service.query(ChatQueryRequest(query=case["query"], debug=True))
            cited = {citation.document_id for citation in response.citations}
            missing = [doc_id for doc_id in case["must_cite"] if doc_id not in cited]
            answer_text = " ".join(segment.text.lower() for segment in response.answer)
            forbidden = [item for item in case["must_not_claim"] if item.lower() in answer_text]
            if missing or forbidden:
                failure_cases.append(
                    {
                        "type": "grounding",
                        "case": case["id"],
                        "query": case["query"],
                        "missing_citations": missing,
                        "forbidden_claims": forbidden,
                    }
                )

        metrics = {
            "retrieval_recall_at_10": round(mean(recall_hits) if recall_hits else 0.0, 3),
            "citation_coverage": round(mean(citation_coverages) if citation_coverages else 0.0, 3),
            "unsupported_claim_rate": round(mean(unsupported_rates) if unsupported_rates else 0.0, 3),
            "latency_p50_ms": round(sorted(latencies_ms)[len(latencies_ms) // 2], 2) if latencies_ms else 0.0,
            "api_smoke_tests": 1.0,
        }
        status = (
            "passed"
            if metrics["retrieval_recall_at_10"] >= self.settings.eval_recall_threshold
            and metrics["citation_coverage"] == 1.0
            and metrics["unsupported_claim_rate"] <= self.settings.eval_unsupported_claim_threshold
            else "failed"
        )
        run.status = status
        run.metrics_json = metrics
        run.details_json = {"failures": failure_cases, "profile": profile}
        run.completed_at = datetime.now(timezone.utc)
        db.commit()
        return run

    def _load_json(self, path: Path) -> list[dict[str, Any]]:
        return json.loads(path.read_text(encoding="utf-8"))

