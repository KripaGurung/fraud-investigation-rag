from enum import Enum

from pydantic import BaseModel

from api.schemas.evidence import EvidenceItem


class EvidenceClassification(str, Enum):
    SUPPORTING = "supporting"
    CONTRADICTING = "contradicting"
    NEUTRAL = "neutral"


class AnalyzedEvidence(BaseModel):
    evidence: EvidenceItem
    classification: EvidenceClassification
    explanation: str
    