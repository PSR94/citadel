from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class IngestionRunSummary(BaseModel):
    id: str
    trigger: str
    status: str
    processed_documents: int
    processed_chunks: int
    error_count: int
    summary: dict[str, Any]
    created_at: datetime
    completed_at: datetime | None

