from __future__ import annotations

from typing import Iterable

from app.services.retrieval.pipeline import SearchHit

try:
    from sentence_transformers import CrossEncoder  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    CrossEncoder = None


class RerankerService:
    def __init__(self) -> None:
        self._model = None

    def available(self) -> bool:
        return CrossEncoder is not None

    def _load(self) -> None:
        if self._model is None and CrossEncoder is not None:
            self._model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query: str, hits: Iterable[SearchHit]) -> list[SearchHit]:
        hits = list(hits)
        if not hits:
            return []
        if not self.available():
            query_terms = {term for term in query.lower().split() if len(term) > 2}
            for hit in hits:
                title_terms = {
                    term for term in hit.document_title.lower().replace("-", " ").split() if len(term) > 2
                }
                text_terms = {term for term in hit.text.lower().split() if len(term) > 2}
                title_overlap = len(query_terms & title_terms) / max(1, len(query_terms))
                text_overlap = len(query_terms & text_terms) / max(1, len(query_terms))
                ownership_boost = 0.12 if "own" in query.lower() and "owner" in hit.text.lower() else 0.0
                hit.rerank_score = (
                    hit.fused_score
                    + hit.graph_boost
                    + (title_overlap * 0.35)
                    + (text_overlap * 0.15)
                    + ownership_boost
                )
            return sorted(hits, key=lambda item: item.rerank_score, reverse=True)

        self._load()
        if not self._model:
            return hits
        scores = self._model.predict([(query, hit.text) for hit in hits])
        for hit, score in zip(hits, scores, strict=False):
            hit.rerank_score = float(score) + hit.graph_boost
        return sorted(hits, key=lambda item: item.rerank_score, reverse=True)
