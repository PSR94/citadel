from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ProviderStateView(BaseModel):
    name: str
    kind: str
    status: str
    latency_ms: float | None
    details: dict[str, Any]
    checked_at: datetime


class PublicConfig(BaseModel):
    app_name: str
    domain: str
    retrieval: dict[str, Any]
    generation: dict[str, Any]
    governance: dict[str, Any]

