from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.documents import DocumentRepository
from app.schemas.documents import ChunkSummary, DocumentDetail, DocumentSummary

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.get("", response_model=list[DocumentSummary])
def list_documents(db: Session = Depends(get_db)) -> list[DocumentSummary]:
    repo = DocumentRepository(db)
    return [
        DocumentSummary(
            id=document.id,
            title=document.title,
            version=document.version,
            owner_team=document.owner_team,
            domain=document.domain,
            source_type=document.source_type,
            access_scope=document.access_scope,
            metadata=document.metadata_json,
            updated_at=document.updated_at,
        )
        for document in repo.list_documents()
    ]


@router.get("/{document_id}", response_model=DocumentDetail)
def get_document(document_id: str, db: Session = Depends(get_db)) -> DocumentDetail:
    repo = DocumentRepository(db)
    document = repo.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
    chunks = repo.list_chunks(document_id)
    return DocumentDetail(
        id=document.id,
        title=document.title,
        version=document.version,
        owner_team=document.owner_team,
        domain=document.domain,
        source_type=document.source_type,
        access_scope=document.access_scope,
        metadata=document.metadata_json,
        updated_at=document.updated_at,
        source_path=document.source_path,
        chunks=[
            ChunkSummary(
                id=chunk.id,
                document_id=chunk.document_id,
                ordinal=chunk.ordinal,
                text=chunk.text,
                token_count=chunk.token_count,
                metadata=chunk.metadata_json,
            )
            for chunk in chunks
        ],
    )


@router.get("/{document_id}/chunks", response_model=list[ChunkSummary])
def get_document_chunks(document_id: str, db: Session = Depends(get_db)) -> list[ChunkSummary]:
    repo = DocumentRepository(db)
    return [
        ChunkSummary(
            id=chunk.id,
            document_id=chunk.document_id,
            ordinal=chunk.ordinal,
            text=chunk.text,
            token_count=chunk.token_count,
            metadata=chunk.metadata_json,
        )
        for chunk in repo.list_chunks(document_id)
    ]

