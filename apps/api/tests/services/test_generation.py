from sqlalchemy.orm import Session

from api.investigation.context import InvestigationContext
from api.investigation.generation.schemas import (
    InvestigationCase,
    InvestigationFinding,
)
from api.services.generation import generate_investigation


class FakeInvestigationGenerator:
    def __init__(self) -> None:
        self.received_alert_id: str | None = None
        self.received_context: InvestigationContext | None = None

    def generate(
        self,
        alert_id: str,
        context: InvestigationContext,
    ) -> InvestigationCase:
        self.received_alert_id = alert_id
        self.received_context = context

        return InvestigationCase(
            alert_id=alert_id,
            executive_summary="Generated investigation summary.",
            risk_narrative="Generated risk narrative.",
            supporting_findings=[
                InvestigationFinding(
                    statement="The transaction is unusual.",
                    evidence_ids=["TXN-004"],
                )
            ],
            missing_evidence=context.missing_evidence,
            recommended_follow_up=["Review the transaction history."],
        )


def test_generate_investigation_orchestrates_existing_pipeline(
    db: Session,
) -> None:
    generator = FakeInvestigationGenerator()

    result = generate_investigation(
        db,
        "ALERT-001",
        generator,
    )

    assert result is not None
    assert result.alert_id == "ALERT-001"
    assert result.executive_summary == "Generated investigation summary."

    assert generator.received_alert_id == "ALERT-001"
    assert generator.received_context is not None

    assert len(generator.received_context.analyzed_evidence) == 5
    assert generator.received_context.missing_evidence == [
        "policy_evidence"
    ]


def test_generate_investigation_returns_none_for_unknown_alert(
    db: Session,
) -> None:
    generator = FakeInvestigationGenerator()

    result = generate_investigation(
        db,
        "ALERT-DOES-NOT-EXIST",
        generator,
    )

    assert result is None
    assert generator.received_alert_id is None
    assert generator.received_context is None