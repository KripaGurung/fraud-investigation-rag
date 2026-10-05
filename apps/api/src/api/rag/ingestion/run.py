from api.db.session import SessionLocal
from api.rag.ingestion.corpus import ingest_corpus


def run_corpus_ingestion() -> None:
    db = SessionLocal()

    try:
        ingest_corpus(db)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_corpus_ingestion()