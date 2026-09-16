from typing import Any

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    source_id: str
    source_type: str
    content: str
    score: float = Field(ge=0.0)
    metadata: dict[str, Any] = Field(default_factory=dict)

class EvidenceBundle(BaseModel):
    alert_id: str
    transaction_evidence: list[EvidenceItem] = Field(default_factory=list)
    historical_case_evidence: list[EvidenceItem] = Field(default_factory=list)
    policy_evidence: list[EvidenceItem] = Field(default_factory=list)    