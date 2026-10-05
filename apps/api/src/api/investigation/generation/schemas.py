from pydantic import BaseModel, Field


class InvestigationFinding(BaseModel):
    """A generated finding grounded in retrieved evidence."""

    statement: str
    evidence_ids: list[str] = Field(default_factory=list)


class InvestigationCase(BaseModel):
    """Structured investigator-ready case generated from investigation context."""

    alert_id: str
    executive_summary: str
    risk_narrative: str
    supporting_findings: list[InvestigationFinding] = Field(default_factory=list)
    contradicting_findings: list[InvestigationFinding] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    recommended_follow_up: list[str] = Field(default_factory=list)