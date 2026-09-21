from sqlalchemy.orm import Session

from api.schemas.evidence import EvidenceBundle
from api.services.evidence import build_evidence_bundle
from api.services.investigation import build_investigation_context


def test_build_evidence_bundle(db: Session) -> None:
    context = build_investigation_context(
        db,
        "ALERT-001",
    )

    assert context is not None

    bundle = build_evidence_bundle(
        db,
        context,
    )

    assert isinstance(bundle, EvidenceBundle)
    assert bundle.alert_id == "ALERT-001"

    assert len(bundle.transaction_evidence) == 2
    assert bundle.historical_case_evidence
    assert bundle.policy_evidence


def test_transaction_evidence_contains_alert_and_transaction(
    db: Session,
) -> None:
    context = build_investigation_context(
        db,
        "ALERT-001",
    )

    assert context is not None

    bundle = build_evidence_bundle(
        db,
        context,
    )

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
    context = build_investigation_context(
        db,
        "ALERT-001",
    )

    assert context is not None

    bundle = build_evidence_bundle(
        db,
        context,
    )

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


def test_historical_evidence_contains_rag_cases(
    db: Session,
) -> None:
    context = build_investigation_context(
        db,
        "ALERT-001",
    )

    assert context is not None

    bundle = build_evidence_bundle(
        db,
        context,
    )

    assert bundle.historical_case_evidence

    assert all(
        evidence.source_type == "historical_fraud_case"
        for evidence in bundle.historical_case_evidence
    )

    source_ids = [
        evidence.source_id
        for evidence in bundle.historical_case_evidence
    ]

    assert any(
        source_id.startswith("CASE-")
        for source_id in source_ids
    )


def test_policy_evidence_contains_rag_policies(
    db: Session,
) -> None:
    context = build_investigation_context(
        db,
        "ALERT-001",
    )

    assert context is not None

    bundle = build_evidence_bundle(
        db,
        context,
    )

    assert bundle.policy_evidence

    assert all(
        evidence.source_type == "aml_policy"
        for evidence in bundle.policy_evidence
    )

    source_ids = [
        evidence.source_id
        for evidence in bundle.policy_evidence
    ]

    assert any(
        source_id.startswith("POLICY-AML-")
        for source_id in source_ids
    )


def test_rag_evidence_contains_provenance(
    db: Session,
) -> None:
    context = build_investigation_context(
        db,
        "ALERT-001",
    )

    assert context is not None

    bundle = build_evidence_bundle(
        db,
        context,
    )

    rag_evidence = (
        bundle.historical_case_evidence
        + bundle.policy_evidence
    )

    assert rag_evidence

    for evidence in rag_evidence:
        assert evidence.score > 0.0
        assert evidence.metadata["title"]
        assert evidence.metadata["source"]
        assert evidence.metadata["chunk_id"] is not None
        assert evidence.metadata["chunk_index"] is not None
        assert 0.0 <= evidence.metadata["semantic_score"] <= 1.0
        assert 0.0 <= evidence.metadata["keyword_score"] <= 1.0


def test_database_transaction_evidence_has_direct_source_score(
    db: Session,
) -> None:
    context = build_investigation_context(
        db,
        "ALERT-001",
    )

    assert context is not None

    bundle = build_evidence_bundle(
        db,
        context,
    )

    assert all(
        evidence.score == 1.0
        for evidence in bundle.transaction_evidence
    )