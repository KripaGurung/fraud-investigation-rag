from pydantic import BaseModel, Field

from api.schemas.evidence import EvidenceItem


class InvestigationResult(BaseModel):
    alert_id: str
    supporting_evidence: list[EvidenceItem] = Field(default_factory=list)
    contradicting_evidence: list[EvidenceItem] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    summary: str