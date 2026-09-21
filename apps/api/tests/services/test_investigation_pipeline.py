import pytest
from sqlalchemy.orm import Session

from api.investigation.schemas import EvidenceClassification
from api.services.investigation_pipeline import run_investigation


def test_run_investigation_returns_result(
    db: Session,
) -> None:
    result = run_investigation(
        db,
        "ALERT-001",
    )

    assert result is not None

    assert result.alert_id == "ALERT-001"
    assert result.summary

    assert result.supporting_evidence
    assert result.missing_evidence == []


def test_run_investigation_includes_rag_historical_cases(
    db: Session,
) -> None:
    result = run_investigation(
        db,
        "ALERT-001",
    )

    assert result is not None

    historical_cases = [
        evidence
        for evidence in result.supporting_evidence
        + result.contradicting_evidence
        if evidence.source_type == "historical_fraud_case"
    ]

    assert historical_cases

    assert all(
        evidence.source_id.startswith("CASE-")
        for evidence in historical_cases
    )


def test_run_investigation_includes_rag_policy_evidence(
    db: Session,
) -> None:
    result = run_investigation(
        db,
        "ALERT-001",
    )

    assert result is not None

    policy_evidence = [
        evidence
        for evidence in result.supporting_evidence
        + result.contradicting_evidence
        if evidence.source_type == "aml_policy"
    ]

    assert policy_evidence

    assert all(
        evidence.source_id.startswith("POLICY-AML-")
        for evidence in policy_evidence
    )


def test_run_investigation_preserves_rag_provenance(
    db: Session,
) -> None:
    result = run_investigation(
        db,
        "ALERT-001",
    )

    assert result is not None

    rag_evidence = [
        evidence
        for evidence in result.supporting_evidence
        + result.contradicting_evidence
        if evidence.source_type
        in {
            "historical_fraud_case",
            "aml_policy",
        }
    ]

    assert rag_evidence

    for evidence in rag_evidence:
        assert evidence.score > 0.0
        assert evidence.metadata["chunk_id"] is not None
        assert evidence.metadata["chunk_index"] is not None
        assert evidence.metadata["title"]
        assert evidence.metadata["source"]


def test_run_investigation_returns_none_for_unknown_alert(
    db: Session,
) -> None:
    result = run_investigation(
        db,
        "ALERT-DOES-NOT-EXIST",
    )

    assert result is None