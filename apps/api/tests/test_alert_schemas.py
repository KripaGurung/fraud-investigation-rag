from datetime import datetime, timezone
from types import SimpleNamespace

from api.schemas.alerts import FraudAlertSummary


def test_fraud_alert_summary_builds_from_attributes() -> None:
    alert = SimpleNamespace(
        alert_reference="ALERT-001",
        alert_type="high_value_transaction",
        severity="high",
        status="open",
        reason="Transaction amount exceeded expected activity.",
        triggered_at=datetime(
            2026,
            1,
            1,
            12,
            0,
            tzinfo=timezone.utc,
        ),
    )

    summary = FraudAlertSummary.model_validate(alert)

    assert summary.alert_reference == "ALERT-001"
    assert summary.alert_type == "high_value_transaction"
    assert summary.severity == "high"
    assert summary.status == "open"
    assert summary.reason == (
        "Transaction amount exceeded expected activity."
    )
    assert summary.triggered_at == alert.triggered_at