from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.config.settings import Settings
from app.models.entities import Chunk, Document, IngestionRun
from app.repositories.documents import DocumentRepository
from app.repositories.runs import RunRepository
from app.services.graph.service import GraphService
from app.services.retrieval.pipeline import LocalRetrievalIndex
from app.utils.hashing import sha256_text
from app.utils.ids import new_id
from app.utils.text import rough_token_count, sentence_windows


class IngestionService:
    def __init__(
        self,
        settings: Settings,
        local_index: LocalRetrievalIndex,
        graph_service: GraphService,
    ) -> None:
        self.settings = settings
        self.local_index = local_index
        self.graph_service = graph_service

    def ingest_directory(self, db: Session, path: Path | None = None, trigger: str = "seed") -> IngestionRun:
        base = path or self.settings.dataset_dir
        run = IngestionRun(
            id=new_id("ingest"),
            trigger=trigger,
            status="running",
            created_at=datetime.now(timezone.utc),
        )
        repo = DocumentRepository(db)
        run_repo = RunRepository(db)
        run_repo.add_ingestion_run(run)
        db.flush()

        processed_documents = 0
        processed_chunks = 0
        graph_payloads: list[dict[str, Any]] = []

        for file_path in sorted(base.rglob("*")):
            if file_path.is_dir() or file_path.name.startswith("."):
                continue
            parsed = self._parse_document(file_path)
            document = Document(
                id=parsed["doc_id"],
                title=parsed["title"],
                version=parsed["version"],
                source_path=str(file_path.relative_to(self.settings.dataset_dir.parent)),
                source_type=file_path.suffix.lstrip(".") or "txt",
                owner_team=parsed.get("owner_team"),
                domain=parsed.get("domain"),
                status="active",
                access_scope=parsed.get("access_scope", "internal"),
                content_hash=sha256_text(parsed["content"]),
                metadata_json=parsed["metadata"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            repo.upsert_document(document)
            chunks = [
                Chunk(
                    id=f"{document.id}-chunk-{index:03d}",
                    document_id=document.id,
                    ordinal=index,
                    text=chunk_text,
                    token_count=rough_token_count(chunk_text),
                    embedding_status="ready",
                    metadata_json={"section": index},
                    created_at=datetime.now(timezone.utc),
                )
                for index, chunk_text in enumerate(sentence_windows(parsed["content"]), start=1)
            ]
            repo.replace_chunks(document.id, chunks)
            graph_payloads.append(
                {
                    "doc_id": document.id,
                    "title": document.title,
                    "owner_team": document.owner_team,
                    "domain": document.domain,
                    "policies": document.metadata_json.get("policies", []),
                    "systems": document.metadata_json.get("systems", []),
                    "references": document.metadata_json.get("references", []),
                }
            )
            processed_documents += 1
            processed_chunks += len(chunks)

        db.commit()
        documents = repo.list_documents()
        self.refresh_runtime_index(db)
        self.graph_service.sync_graph(graph_payloads)

        run.status = "completed"
        run.processed_documents = processed_documents
        run.processed_chunks = processed_chunks
        run.summary_json = {
            "dataset_path": str(base),
            "documents": processed_documents,
            "chunks": processed_chunks,
        }
        run.completed_at = datetime.now(timezone.utc)
        db.commit()
        return run

    def refresh_runtime_index(self, db: Session) -> None:
        repo = DocumentRepository(db)
        documents = repo.list_documents()
        all_chunks = [chunk for document in documents for chunk in repo.list_chunks(document.id)]
        self.local_index.refresh(documents, all_chunks)

    def _parse_document(self, path: Path) -> dict[str, Any]:
        if path.suffix == ".md":
            return self._parse_markdown(path)
        if path.suffix == ".json":
            return self._parse_json(path)
        if path.suffix == ".pdf":
            return self._parse_pdf(path)
        return self._parse_text(path)

    def _parse_markdown(self, path: Path) -> dict[str, Any]:
        raw = path.read_text(encoding="utf-8")
        metadata: dict[str, Any] = {}
        content = raw
        if raw.startswith("---"):
            _, yaml_blob, content = raw.split("---", 2)
            metadata = yaml.safe_load(yaml_blob) or {}
        content = content.strip()
        return self._assembled_payload(path, metadata, content)

    def _parse_json(self, path: Path) -> dict[str, Any]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        content = "\n\n".join(
            f"{section['heading']}\n{section['content']}" for section in payload.get("sections", [])
        )
        return self._assembled_payload(path, payload, content)

    def _parse_text(self, path: Path) -> dict[str, Any]:
        raw = path.read_text(encoding="utf-8")
        lines = raw.splitlines()
        metadata: dict[str, Any] = {"references": []}
        content_lines: list[str] = []
        for line in lines:
            if ":" in line and line.split(":", 1)[0].isupper():
                key, value = line.split(":", 1)
                normalized = key.lower()
                if normalized == "references":
                    metadata[normalized] = [item.strip() for item in value.split(",") if item.strip()]
                else:
                    metadata[normalized] = value.strip()
            else:
                content_lines.append(line)
        return self._assembled_payload(path, metadata, "\n".join(content_lines).strip())

    def _parse_pdf(self, path: Path) -> dict[str, Any]:
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        metadata = {
            "doc_id": path.stem.upper().replace("_", "-"),
            "title": path.stem.replace("-", " ").title(),
            "version": "1.0",
        }
        return self._assembled_payload(path, metadata, text)

    def _assembled_payload(self, path: Path, metadata: dict[str, Any], content: str) -> dict[str, Any]:
        doc_id = metadata.get("doc_id") or path.stem.upper().replace("_", "-")
        title = metadata.get("title") or path.stem.replace("-", " ").title()
        version = str(metadata.get("version", "1.0"))
        assembled = {
            "doc_id": doc_id,
            "title": title,
            "version": version,
            "owner_team": metadata.get("owner_team"),
            "domain": metadata.get("domain"),
            "access_scope": metadata.get("access_scope", "internal"),
            "content": content,
            "metadata": {
                "systems": metadata.get("systems", []),
                "policies": metadata.get("policies", []),
                "references": metadata.get("references", []),
                "supersedes": metadata.get("supersedes", []),
                "superseded_by": metadata.get("superseded_by", []),
                "owner_team": metadata.get("owner_team"),
                "domain": metadata.get("domain"),
                "title": title,
            },
        }
        return assembled
