from sqlalchemy.orm import Session

from api.rag.corpus.historical_cases import HISTORICAL_FRAUD_CASES
from api.rag.corpus.policies import AML_FRAUD_POLICIES
from api.rag.corpus.schema import CorpusDocument
from api.rag.ingestion.pipeline import ingest_document


CORPUS_DOCUMENTS: tuple[CorpusDocument, ...] = (
    *HISTORICAL_FRAUD_CASES,
    *AML_FRAUD_POLICIES,
)


def ingest_corpus(db: Session) -> None:
    for document in CORPUS_DOCUMENTS:
        ingest_document(
            db=db,
            document=document,
        )