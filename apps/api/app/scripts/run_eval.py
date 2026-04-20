from __future__ import annotations

import argparse

from app.core.dependencies import get_container
from app.db.base import Base
from app.db.session import SessionLocal, engine


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="ci")
    args = parser.parse_args()

    Base.metadata.create_all(bind=engine)
    container = get_container()
    with SessionLocal() as db:
        if not container.local_index.ready():
            container.ingestion.ingest_directory(db, trigger="eval-bootstrap")
        run = container.evals(db).run(db, profile=args.profile)
    print({"eval_id": run.id, "status": run.status, "metrics": run.metrics_json})


if __name__ == "__main__":
    main()

