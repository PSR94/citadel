from __future__ import annotations

from dataclasses import asdict
from time import perf_counter
from typing import Any

from sqlalchemy.orm import Session

from app.core.logging import logger
from app.models.entities import AuditEvent, RetrievalRun
from app.repositories.runs import RunRepository
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse, QueryDebugTrace
from app.services.chat.debug_orchestrator import DebugPolicy
from app.services.citations.service import CitationService
from app.services.policy.guardrails import GuardrailService
from app.services.retrieval.pipeline import LocalRetrievalIndex, SearchHit, merge_hits
from app.services.reranking.service import RerankerService
from app.utils.ids import new_id
from app.utils.text import normalize_query


class ChatService:
    def __init__(
        self,
        db: Session,
        local_index: LocalRetrievalIndex,
        reranker: RerankerService,
        citation_service: CitationService,
        guardrails: GuardrailService,
    ) -> None:
        self.db = db
        self.local_index = local_index
        self.reranker = reranker
        self.citation_service = citation_service
        self.guardrails = guardrails

    def query(self, request: ChatQueryRequest, graph_hops: int = 1) -> ChatQueryResponse:
        started = perf_counter()
        timings: dict[str, float] = {}

        normalized_query = normalize_query(request.query)
        timings["normalize"] = (perf_counter() - started) * 1000

        rewritten_queries = self._rewrite_query(normalized_query)
        timings["rewrite"] = (perf_counter() - started) * 1000 - sum(timings.values())

        lexical_hits: list[SearchHit] = []
        dense_hits: list[SearchHit] = []
        for rewritten_query in rewritten_queries:
            lexical_hits.extend(self.local_index.lexical_search(rewritten_query, request.top_k or 12))
            dense_hits.extend(self.local_index.dense_search(rewritten_query, request.top_k or 12))
        timings["retrieve"] = (perf_counter() - started) * 1000 - sum(timings.values())

        fused_hits = merge_hits(lexical_hits, dense_hits)
        graph_notes = self.local_index.graph_expand(
            normalized_query, [hit.document_id for hit in fused_hits[:4]], graph_hops
        )
        self._apply_graph_boosts(fused_hits, graph_notes)
        timings["graph"] = (perf_counter() - started) * 1000 - sum(timings.values())

        reranked_hits = self.reranker.rerank(normalized_query, fused_hits[: max(request.top_k or 12, 8)])
        timings["rerank"] = (perf_counter() - started) * 1000 - sum(timings.values())

        answer, citations, evidence, grounding = self.citation_service.build_answer(
            normalized_query,
            reranked_hits,
            request.max_citations,
        )
        timings["answer"] = (perf_counter() - started) * 1000 - sum(timings.values())

        status = "grounded"
        if grounding.insufficient_evidence:
            status = "insufficient_evidence"

        debug_policy = DebugPolicy(max_graph_hops=graph_hops)
        response = ChatQueryResponse(
            run_id=new_id("run"),
            status=status,
            answer=answer,
            citations=citations,
            evidence=evidence,
            grounding=grounding,
            debug=QueryDebugTrace(
                normalized_query=normalized_query,
                rewritten_queries=rewritten_queries,
                graph_expansion=[asdict(note) for note in graph_notes],
                stage_timings_ms={key: round(value, 2) for key, value in timings.items()},
                policy_notes=debug_policy.notes() + self.guardrails.validate_query(request),
            ),
            provider={
                "generator": "extractive",
                "reranker": "cross-encoder" if self.reranker.available() else "fusion-score fallback",
            },
        )
        self._persist_run(request, response)
        return response

    def _rewrite_query(self, query: str) -> list[str]:
        rewritten = [query]
        if "sev 1" in query.lower():
            rewritten.append(query.lower().replace("sev 1", "severity 1"))
        if "rollback" in query.lower():
            rewritten.append(f"{query} deployment platform")
        return list(dict.fromkeys(rewritten))

    def _apply_graph_boosts(self, hits: list[SearchHit], notes) -> None:
        related_docs = {note.related_document_id for note in notes}
        for hit in hits:
            if hit.document_id in related_docs:
                hit.graph_boost = 0.1
                hit.fused_score += hit.graph_boost

    def _persist_run(self, request: ChatQueryRequest, response: ChatQueryResponse) -> None:
        run = RetrievalRun(
            id=response.run_id,
            query=request.query,
            status=response.status,
            request_json=request.model_dump(),
            response_json=response.model_dump(),
            timings_json=response.debug.stage_timings_ms,
            provider_json=response.provider,
        )
        repo = RunRepository(self.db)
        repo.add_retrieval_run(run)
        repo.add_audit_event(
            AuditEvent(
                id=new_id("audit"),
                event_type="chat.query",
                actor="local-operator",
                resource=response.run_id,
                payload_json={"query": request.query, "status": response.status},
            )
        )
        self.db.commit()
        logger.info("chat_query_completed", run_id=response.run_id, status=response.status)
