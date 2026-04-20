from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ActorContext:
    subject: str = "local-operator"
    role: str = "admin"
    scopes: tuple[str, ...] = ("documents:read", "chat:query", "evals:run", "ingest:write")


def default_actor() -> ActorContext:
    return ActorContext()

