from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Any

import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.entities import Chunk, Document
from app.utils.text import normalize_query


@dataclass(slots=True)
class SearchHit:
    chunk_id: str
    document_id: str
    document_title: str
    text: str
    source_path: str
    metadata: dict[str, Any]
    lexical_score: float = 0.0
    dense_score: float = 0.0
    fused_score: float = 0.0
    rerank_score: float = 0.0
    graph_boost: float = 0.0

    def score_payload(self) -> dict[str, float]:
        return {
            "lexical": self.lexical_score,
            "dense": self.dense_score,
            "fusion": self.fused_score,
            "graph_boost": self.graph_boost,
            "rerank": self.rerank_score,
        }


@dataclass(slots=True)
class GraphExpansionNote:
    source_node: str
    related_document_id: str
    relation: str
    gain: str


@dataclass(slots=True)
class RetrievalState:
    vectorizer: TfidfVectorizer | None = None
    matrix: Any = None
    dense_vectorizer: TfidfVectorizer | None = None
    dense_matrix: Any = None
    chunks: list[SearchHit] = field(default_factory=list)
    graph: nx.MultiDiGraph = field(default_factory=nx.MultiDiGraph)
    refreshed_at: float = 0.0


class LocalRetrievalIndex:
    def __init__(self) -> None:
        self.state = RetrievalState()

    def refresh(self, documents: list[Document], chunks: list[Chunk]) -> None:
        hits: list[SearchHit] = []
        graph = nx.MultiDiGraph()
        documents_by_id = {document.id: document for document in documents}

        for document in documents:
            graph.add_node(document.id, kind="document", label=document.title)
            metadata = document.metadata_json or {}
            for system in metadata.get("systems", []):
                graph.add_node(system, kind="system", label=system)
                graph.add_edge(document.id, system, relation="mentions")
                graph.add_edge(system, document.id, relation="mentioned_by")
            for policy in metadata.get("policies", []):
                graph.add_node(policy, kind="policy", label=policy)
                graph.add_edge(document.id, policy, relation="governed_by")
                graph.add_edge(policy, document.id, relation="governs")
            for reference in metadata.get("references", []):
                if reference in documents_by_id:
                    graph.add_edge(document.id, reference, relation="references")
                    graph.add_edge(reference, document.id, relation="referenced_by")
            for supersedes in metadata.get("supersedes", []):
                graph.add_edge(document.id, supersedes, relation="supersedes")
                graph.add_edge(supersedes, document.id, relation="superseded_by")
            for superseded_by in metadata.get("superseded_by", []):
                graph.add_edge(document.id, superseded_by, relation="superseded_by")
                graph.add_edge(superseded_by, document.id, relation="supersedes")
            if document.owner_team:
                team = document.owner_team
                graph.add_node(team, kind="team", label=team)
                graph.add_edge(document.id, team, relation="owned_by")
                graph.add_edge(team, document.id, relation="owns")

        for chunk in chunks:
            document = documents_by_id.get(chunk.document_id)
            if not document:
                continue
            hits.append(
                SearchHit(
                    chunk_id=chunk.id,
                    document_id=document.id,
                    document_title=document.title,
                    text=chunk.text,
                    source_path=document.source_path,
                    metadata={
                        **(document.metadata_json or {}),
                        **(chunk.metadata_json or {}),
                    },
                )
            )

        corpus = [hit.text for hit in hits] or [""]
        lexical_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        dense_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 3), sublinear_tf=True)
        self.state = RetrievalState(
            vectorizer=lexical_vectorizer,
            matrix=lexical_vectorizer.fit_transform(corpus),
            dense_vectorizer=dense_vectorizer,
            dense_matrix=dense_vectorizer.fit_transform(corpus),
            chunks=hits,
            graph=graph,
            refreshed_at=perf_counter(),
        )

    def ready(self) -> bool:
        return bool(self.state.chunks and self.state.vectorizer and self.state.dense_vectorizer)

    def lexical_search(self, query: str, top_k: int) -> list[SearchHit]:
        if not self.ready() or not self.state.vectorizer:
            return []
        query_vector = self.state.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.state.matrix).flatten()
        return self._top_hits(scores, top_k, score_key="lexical")

    def dense_search(self, query: str, top_k: int) -> list[SearchHit]:
        if not self.ready() or not self.state.dense_vectorizer:
            return []
        query_vector = self.state.dense_vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.state.dense_matrix).flatten()
        return self._top_hits(scores, top_k, score_key="dense")

    def graph_expand(self, query: str, seed_document_ids: list[str], hops: int) -> list[GraphExpansionNote]:
        query_terms = set(normalize_query(query).lower().split())
        notes: list[GraphExpansionNote] = []
        graph = self.state.graph
        if not graph.nodes:
            return notes

        entry_nodes = set(seed_document_ids)
        for node, data in graph.nodes(data=True):
            label = str(data.get("label", node)).lower()
            if query_terms & set(label.split()):
                entry_nodes.add(node)

        visited: set[str] = set()
        frontier = list(entry_nodes)
        for _ in range(max(1, hops)):
            next_frontier: list[str] = []
            for node in frontier:
                if node in visited or node not in graph:
                    continue
                visited.add(node)
                for _, neighbor, edge_data in graph.out_edges(node, data=True):
                    relation = str(edge_data.get("relation", "related_to"))
                    next_frontier.append(neighbor)
                    if str(neighbor).startswith("DOC-"):
                        notes.append(
                            GraphExpansionNote(
                                source_node=str(node),
                                related_document_id=str(neighbor),
                                relation=relation,
                                gain="Related governance or ownership context",
                            )
                        )
            frontier = next_frontier
        return notes

    def get_hit(self, chunk_id: str) -> SearchHit | None:
        for hit in self.state.chunks:
            if hit.chunk_id == chunk_id:
                return hit
        return None

    def _top_hits(self, scores: np.ndarray, top_k: int, score_key: str) -> list[SearchHit]:
        indexes = np.argsort(scores)[::-1][:top_k]
        hits: list[SearchHit] = []
        for index in indexes:
            if scores[index] <= 0:
                continue
            hit = self.state.chunks[index]
            copied = SearchHit(**asdict(hit))
            if score_key == "lexical":
                copied.lexical_score = float(scores[index])
            else:
                copied.dense_score = float(scores[index])
            hits.append(copied)
        return hits


def merge_hits(lexical_hits: list[SearchHit], dense_hits: list[SearchHit]) -> list[SearchHit]:
    by_chunk: dict[str, SearchHit] = {}
    for hit in lexical_hits + dense_hits:
        existing = by_chunk.get(hit.chunk_id)
        if not existing:
            by_chunk[hit.chunk_id] = SearchHit(**asdict(hit))
            existing = by_chunk[hit.chunk_id]
        existing.lexical_score = max(existing.lexical_score, hit.lexical_score)
        existing.dense_score = max(existing.dense_score, hit.dense_score)
        existing.fused_score = (existing.lexical_score * 0.45) + (existing.dense_score * 0.55)
    return sorted(by_chunk.values(), key=lambda item: item.fused_score, reverse=True)
