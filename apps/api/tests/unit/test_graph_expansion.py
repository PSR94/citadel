from app.services.retrieval.pipeline import LocalRetrievalIndex
from app.db.session import SessionLocal


def test_graph_expansion_finds_related_adr_document():
    with SessionLocal() as db:
        from app.repositories.documents import DocumentRepository

        repo = DocumentRepository(db)
        docs = repo.list_documents()
        chunks = [chunk for doc in docs for chunk in repo.list_chunks(doc.id)]
        index = LocalRetrievalIndex()
        index.refresh(docs, chunks)

        notes = index.graph_expand("Which ADR replaced the legacy auth proxy?", ["DOC-ADR-001"], hops=1)

    assert any(note.related_document_id == "DOC-ADR-006" for note in notes)

