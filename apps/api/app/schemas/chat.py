from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatQueryRequest(BaseModel):
    query: str = Field(min_length=3, max_length=2000)
    debug: bool = False
    max_citations: int = Field(default=6, ge=1, le=12)
    top_k: int | None = Field(default=None, ge=2, le=20)
    use_graph_expansion: bool = True


class Citation(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    span: str
    score: float


class AnswerSegment(BaseModel):
    text: str
    citations: list[Citation]
    supported: bool = True


class EvidenceChunk(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    text: str
    scores: dict[str, float]
    source_path: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class GroundingStatus(BaseModel):
    citation_coverage: float
    unsupported_claims: int
    insufficient_evidence: bool
    rationale: list[str]


class QueryDebugTrace(BaseModel):
    normalized_query: str
    rewritten_queries: list[str]
    graph_expansion: list[dict[str, Any]]
    stage_timings_ms: dict[str, float]
    policy_notes: list[str]


class ChatQueryResponse(BaseModel):
    run_id: str
    status: Literal["grounded", "insufficient_evidence", "provider_unavailable"]
    answer: list[AnswerSegment]
    citations: list[Citation]
    evidence: list[EvidenceChunk]
    grounding: GroundingStatus
    debug: QueryDebugTrace
    provider: dict[str, Any]

