from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models import KnowledgeChunk, KnowledgeDocument
from api.rag.corpus.schema import CorpusDocument
from api.rag.ingestion.chunking import chunk_text


def ingest_document(
    db: Session,
    document: CorpusDocument,
) -> None:
    statement = select(KnowledgeDocument).where(
        KnowledgeDocument.document_reference
        == document.document_reference
    )

    existing_document = db.scalar(statement)

    if existing_document is not None:
        return

    knowledge_document = KnowledgeDocument(
        document_reference=document.document_reference,
        document_type=document.document_type,
        title=document.title,
        source=document.source,
        content=document.content,
    )

    db.add(knowledge_document)

    text_chunks = chunk_text(document.content)

    for text_chunk in text_chunks:
        knowledge_chunk = KnowledgeChunk(
            document=knowledge_document,
            chunk_index=text_chunk.chunk_index,
            content=text_chunk.content,
        )

        db.add(knowledge_chunk)
