from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FraudAlertSummary(BaseModel):
    """Investigator-facing summary of a fraud alert."""

    model_config = ConfigDict(from_attributes=True)

    alert_reference: str
    alert_type: str
    severity: str
    status: str
    reason: str
    triggered_at: datetime