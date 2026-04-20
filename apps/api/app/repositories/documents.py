from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.entities import Chunk, Document


class DocumentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_documents(self) -> list[Document]:
        stmt = select(Document).order_by(Document.updated_at.desc())
        return list(self.db.scalars(stmt))

    def get_document(self, document_id: str) -> Document | None:
        stmt = select(Document).options(selectinload(Document.chunks)).where(Document.id == document_id)
        return self.db.scalars(stmt).first()

    def list_chunks(self, document_id: str) -> list[Chunk]:
        stmt = select(Chunk).where(Chunk.document_id == document_id).order_by(Chunk.ordinal.asc())
        return list(self.db.scalars(stmt))

    def upsert_document(self, document: Document) -> Document:
        current = self.db.get(Document, document.id)
        if current:
            for field in (
                "title",
                "version",
                "source_path",
                "source_type",
                "owner_team",
                "domain",
                "status",
                "access_scope",
                "content_hash",
                "metadata_json",
                "updated_at",
            ):
                setattr(current, field, getattr(document, field))
            return current
        self.db.add(document)
        return document

    def replace_chunks(self, document_id: str, chunks: list[Chunk]) -> None:
        self.db.query(Chunk).filter(Chunk.document_id == document_id).delete()
        self.db.add_all(chunks)

