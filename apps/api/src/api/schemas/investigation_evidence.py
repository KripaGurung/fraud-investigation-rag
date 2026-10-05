from pydantic import BaseModel, Field

from api.investigation.schemas import AnalyzedEvidence


class InvestigationEvidenceResponse(BaseModel):
    """Analyzed evidence available for an investigation."""

    alert_id: str
    analyzed_evidence: list[AnalyzedEvidence] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)