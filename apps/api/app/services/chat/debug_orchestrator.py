from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DebugPolicy:
    max_graph_hops: int = 1
    allow_query_rewrite: bool = True
    allow_source_exploration: bool = True
    timeout_seconds: int = 12

    def notes(self) -> list[str]:
        return [
            f"Graph expansion limited to {self.max_graph_hops} hop(s).",
            "Query rewriting is bounded and retrieval-only.",
            "No autonomous tool execution is permitted outside retrieval diagnostics.",
        ]

