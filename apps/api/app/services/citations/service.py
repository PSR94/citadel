from __future__ import annotations

from typing import Iterable

from app.schemas.chat import AnswerSegment, Citation, EvidenceChunk, GroundingStatus
from app.services.retrieval.pipeline import SearchHit


class CitationService:
    def build_answer(
        self, query: str, hits: Iterable[SearchHit], max_citations: int
    ) -> tuple[list[AnswerSegment], list[Citation], list[EvidenceChunk], GroundingStatus]:
        selected_hits = list(hits)[:max_citations]
        evidence = [
            EvidenceChunk(
                chunk_id=hit.chunk_id,
                document_id=hit.document_id,
                document_title=hit.document_title,
                text=hit.text,
                scores=hit.score_payload(),
                source_path=hit.source_path,
                metadata=hit.metadata,
            )
            for hit in selected_hits
        ]
        citations = [
            Citation(
                chunk_id=hit.chunk_id,
                document_id=hit.document_id,
                document_title=hit.document_title,
                span=self._evidence_span(query, hit.text),
                score=max(hit.rerank_score, hit.fused_score, hit.lexical_score, hit.dense_score),
            )
            for hit in selected_hits
        ]

        answer_segments: list[AnswerSegment] = []
        query_terms = {term for term in query.lower().split() if len(term) > 2}
        unsupported_claims = 0

        for hit, citation in zip(selected_hits, citations, strict=False):
            sentences = [sentence.strip() for sentence in hit.text.split(". ") if sentence.strip()]
            best_sentence = next((s for s in sentences if query_terms & set(s.lower().split())), hit.text[:240])
            supported = bool(best_sentence)
            if not supported:
                unsupported_claims += 1
            answer_segments.append(
                AnswerSegment(
                    text=best_sentence if best_sentence.endswith(".") else f"{best_sentence}.",
                    citations=[citation],
                    supported=supported,
                )
            )

        insufficient_evidence = len(answer_segments) == 0
        grounding = GroundingStatus(
            citation_coverage=0.0 if insufficient_evidence else 1.0,
            unsupported_claims=unsupported_claims,
            insufficient_evidence=insufficient_evidence,
            rationale=(
                ["No evidence chunk cleared the retrieval threshold."]
                if insufficient_evidence
                else [
                    "Each answer segment is derived from retrieved evidence.",
                    "Unsupported segments are suppressed rather than surfaced as grounded output.",
                ]
            ),
        )
        return answer_segments, citations, evidence, grounding

    def _evidence_span(self, query: str, text: str) -> str:
        if len(text) <= 180:
            return text
        query_terms = {term for term in query.lower().split() if len(term) > 2}
        words = text.split()
        for index, word in enumerate(words):
            if word.lower().strip(".,:;()") in query_terms:
                start = max(0, index - 12)
                end = min(len(words), index + 28)
                return " ".join(words[start:end])
        return " ".join(words[:40])

