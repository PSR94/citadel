from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(APIModel):
    error: str
    detail: str
    request_id: str | None = None


class StatusResponse(APIModel):
    status: str
    detail: str
    checked_at: datetime
    details: dict[str, Any] = Field(default_factory=dict)

