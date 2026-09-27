from sqlalchemy.orm import Session

from api.services.investigation_evidence import (
    get_investigation_evidence,
)


def test_get_investigation_evidence_returns_analyzed_evidence(
    db: Session,
) -> None:
    result = get_investigation_evidence(
        db,
        "ALERT-001",
    )

    assert result is not None
    assert result.alert_id == "ALERT-001"
    assert len(result.analyzed_evidence) > 0
    assert result.missing_evidence == ["policy_evidence"]

def test_get_investigation_evidence_returns_none_for_unknown_alert(
    db: Session,
) -> None:
    result = get_investigation_evidence(
        db,
        "ALERT-DOES-NOT-EXIST",
    )

    assert result is None    