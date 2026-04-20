from __future__ import annotations

from app.core.dependencies import get_container
from app.db.base import Base
from app.db.session import SessionLocal, engine


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        run = get_container().ingestion.ingest_directory(db, trigger="script")
    print({"run_id": run.id, "documents": run.processed_documents, "chunks": run.processed_chunks})


if __name__ == "__main__":
    main()

