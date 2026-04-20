from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select

from app.api.v1.router import api_router
from app.config.settings import get_settings
from app.core.dependencies import get_container
from app.core.logging import configure_logging
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.entities import Document

settings = get_settings()
configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        document_count = db.scalar(select(func.count()).select_from(Document)) or 0
        container = get_container()
        if not document_count:
            container.ingestion.ingest_directory(db, trigger="startup")
        else:
            container.ingestion.refresh_runtime_index(db)
    yield


app = FastAPI(title="CITADEL API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
