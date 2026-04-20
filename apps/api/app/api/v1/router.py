from fastapi import APIRouter

from app.api.v1.routes import chat, documents, evals, health, ingest, providers, retrieval

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(chat.router)
api_router.include_router(ingest.router)
api_router.include_router(documents.router)
api_router.include_router(retrieval.router)
api_router.include_router(evals.router)
api_router.include_router(providers.router)

