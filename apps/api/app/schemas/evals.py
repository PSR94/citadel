from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class EvalRunRequest(BaseModel):
    profile: str = "ci"


class EvalRunSummary(BaseModel):
    id: str
    profile: str
    status: str
    metrics: dict[str, float]
    created_at: datetime
    completed_at: datetime | None


class EvalRunDetail(EvalRunSummary):
    details: dict[str, Any]

