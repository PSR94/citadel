from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from neo4j import GraphDatabase

from app.config.settings import Settings
from app.core.logging import logger
from app.services.retrieval.pipeline import GraphExpansionNote


class GraphService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_username, settings.neo4j_password),
            )
        except Exception:
            self.driver = None

    def available(self) -> bool:
        return self.driver is not None

    def ping(self) -> tuple[str, dict]:
        if not self.driver:
            return "degraded", {"reason": "Neo4j driver unavailable or disabled"}
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 AS ok").single()
            return ("healthy", {"bolt": bool(result and result["ok"] == 1)})
        except Exception as exc:  # pragma: no cover - network
            return "degraded", {"reason": str(exc)}

    def sync_graph(self, documents: Iterable[dict]) -> None:
        if not self.driver:
            return
        query = """
        MERGE (d:Document {id: $doc_id})
        SET d.title = $title, d.owner_team = $owner_team, d.domain = $domain
        WITH d
        FOREACH (policy IN $policies |
          MERGE (p:Policy {id: policy})
          MERGE (d)-[:GOVERNED_BY]->(p))
        FOREACH (system IN $systems |
          MERGE (s:System {name: system})
          MERGE (d)-[:MENTIONS]->(s))
        FOREACH (ref_id IN $references |
          MERGE (r:Document {id: ref_id})
          MERGE (d)-[:REFERENCES]->(r))
        FOREACH (team_name IN CASE WHEN $owner_team IS NULL THEN [] ELSE [$owner_team] END |
          MERGE (t:Team {name: team_name})
          MERGE (d)-[:OWNED_BY]->(t))
        """
        try:
            with self.driver.session() as session:
                for document in documents:
                    session.run(query, **document)
        except Exception as exc:  # pragma: no cover - network
            logger.warning("neo4j_sync_failed", error=str(exc))

    def format_notes(self, notes: Iterable[GraphExpansionNote]) -> list[dict]:
        return [asdict(note) for note in notes]

