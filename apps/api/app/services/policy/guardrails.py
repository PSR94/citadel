from __future__ import annotations

from app.schemas.chat import ChatQueryRequest


class GuardrailService:
    def validate_query(self, request: ChatQueryRequest) -> list[str]:
        notes: list[str] = []
        lowered = request.query.lower()
        if "delete all" in lowered or "run shell" in lowered:
            notes.append("Tool execution requests are outside the retrieval policy boundary.")
        if "export all employee data" in lowered:
            notes.append("Bulk data export is blocked in the governance-aware retrieval profile.")
        return notes

