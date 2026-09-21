from sqlalchemy.orm import Session

from api.schemas.evidence import EvidenceBundle
from api.services.evidence import build_evidence_bundle
from api.services.investigation import build_investigation_context


def test_build_evidence_bundle(db: Session) -> None:
    context = build_investigation_context(db, "ALERT-001")

    assert context is not None

    bundle = build_evidence_bundle(context)

    assert isinstance(bundle, EvidenceBundle)
    assert bundle.alert_id == "ALERT-001"

    assert len(bundle.transaction_evidence) == 2
    assert len(bundle.historical_case_evidence) == 3
    assert len(bundle.policy_evidence) == 0


def test_transaction_evidence_contains_alert_and_transaction(
    db: Session,
) -> None:
    context = build_investigation_context(db, "ALERT-001")

    assert context is not None

    bundle = build_evidence_bundle(context)

    source_ids = [
        evidence.source_id
        for evidence in bundle.transaction_evidence
    ]

    assert source_ids == [
        "ALERT-001",
        "TXN-004",
    ]


def test_transaction_evidence_contains_expected_facts(
    db: Session,
) -> None:
    context = build_investigation_context(db, "ALERT-001")

    assert context is not None

    bundle = build_evidence_bundle(context)

    alert_evidence = bundle.transaction_evidence[0]
    transaction_evidence = bundle.transaction_evidence[1]

    assert alert_evidence.source_type == "fraud_alert"
    assert "high_amount" in alert_evidence.content
    assert "high" in alert_evidence.content

    assert transaction_evidence.source_type == "transaction"
    assert "450000.00 NPR" in transaction_evidence.content
    assert "Singapore, SG" in transaction_evidence.content
    assert "DEVICE-UNKNOWN-99" in transaction_evidence.content
    assert "web" in transaction_evidence.content


def test_historical_evidence_contains_expected_transactions(
    db: Session,
) -> None:
    context = build_investigation_context(db, "ALERT-001")

    assert context is not None

    bundle = build_evidence_bundle(context)

    source_ids = [
        evidence.source_id
        for evidence in bundle.historical_case_evidence
    ]

    assert source_ids == [
        "TXN-003",
        "TXN-002",
        "TXN-001",
    ]


def test_historical_evidence_contains_expected_facts(
    db: Session,
) -> None:
    context = build_investigation_context(db, "ALERT-001")

    assert context is not None

    bundle = build_evidence_bundle(context)

    evidence_by_source = {
        evidence.source_id: evidence
        for evidence in bundle.historical_case_evidence
    }

    assert "3800.00 NPR" in evidence_by_source["TXN-003"].content
    assert "6200.00 NPR" in evidence_by_source["TXN-002"].content
    assert "4500.00 NPR" in evidence_by_source["TXN-001"].content

    assert "Kathmandu, NP" in evidence_by_source["TXN-003"].content
    assert "DEVICE-MAYA-01" in evidence_by_source["TXN-003"].content


def test_all_database_evidence_has_direct_source_score(
    db: Session,
) -> None:
    context = build_investigation_context(db, "ALERT-001")

    assert context is not None

    bundle = build_evidence_bundle(context)

    all_evidence = (
        bundle.transaction_evidence
        + bundle.historical_case_evidence
        + bundle.policy_evidence
    )

    assert all(evidence.score == 1.0 for evidence in all_evidence)