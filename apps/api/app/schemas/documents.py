from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class DocumentSummary(BaseModel):
    id: str
    title: str
    version: str
    owner_team: str | None
    domain: str | None
    source_type: str
    access_scope: str
    metadata: dict[str, Any]
    updated_at: datetime


class ChunkSummary(BaseModel):
    id: str
    document_id: str
    ordinal: int
    text: str
    token_count: int
    metadata: dict[str, Any]


class DocumentDetail(DocumentSummary):
    source_path: str
    chunks: list[ChunkSummary]

