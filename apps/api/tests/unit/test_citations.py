from app.schemas.chat import ChatQueryRequest
from app.services.chat.service import ChatService
from app.services.citations.service import CitationService
from app.services.policy.guardrails import GuardrailService
from app.services.retrieval.pipeline import LocalRetrievalIndex
from app.services.reranking.service import RerankerService
from app.db.session import SessionLocal


def test_grounded_answer_contains_citations():
    with SessionLocal() as db:
        local_index = LocalRetrievalIndex()
        from app.repositories.documents import DocumentRepository

        repo = DocumentRepository(db)
        docs = repo.list_documents()
        chunks = [chunk for doc in docs for chunk in repo.list_chunks(doc.id)]
        local_index.refresh(docs, chunks)
        service = ChatService(db, local_index, RerankerService(), CitationService(), GuardrailService())
        response = service.query(
            ChatQueryRequest(query="Which team owns the deployment rollback runbook?")
        )

    assert response.answer
    assert all(segment.citations for segment in response.answer)
    assert response.citations[0].document_id == "DOC-PLAT-002"
