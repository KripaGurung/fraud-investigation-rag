from dataclasses import dataclass


@dataclass(frozen=True)
class CorpusDocument:
    document_reference: str
    document_type: str
    title: str
    source: str
    content: str
