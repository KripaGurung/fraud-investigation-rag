from unittest.mock import Mock

from sqlalchemy.orm import Session

from api.rag.retrieval.hybrid import HybridSearchResult
from api.schemas.evidence import EvidenceBundle
from api.services.evidence import build_evidence_bundle
from api.services.investigation import build_investigation_context


def test_evidence_bundle_includes_rag_historical_and_policy_evidence(
    db: Session,
    monkeypatch,
) -> None:
    historical_result = HybridSearchResult(
        chunk_id=101,
        document_reference="CASE-001",
        document_type="historical_fraud_case",
        title="Large International Transfer from Previously Domestic Account",
        source="synthetic_historical_case_corpus",
        chunk_index=0,
        content="A high-value international transfer involved a new beneficiary.",
        semantic_score=0.90,
        keyword_score=0.80,
        score=0.87,
    )

    policy_result = HybridSearchResult(
        chunk_id=201,
        document_reference="POLICY-AML-001",
        document_type="aml_policy",
        title="Monitoring Significant Deviations from Customer Transaction Patterns",
        source="synthetic_aml_policy_corpus",
        chunk_index=0,
        content="Significant deviations from established transaction patterns may warrant review.",
        semantic_score=0.88,
        keyword_score=0.75,
        score=0.841,
    )

    def mock_hybrid_search(
        db,
        query,
        limit,
        document_type,
    ):
        if document_type == "historical_fraud_case":
            return [historical_result]

        if document_type == "aml_policy":
            return [policy_result]

        return []

    monkeypatch.setattr(
        "api.services.evidence.hybrid_search",
        mock_hybrid_search,
    )

    context = build_investigation_context(
        db,
        "ALERT-001",
    )

    assert context is not None

    bundle = build_evidence_bundle(db, context)

    assert isinstance(bundle, EvidenceBundle)

    assert len(bundle.transaction_evidence) == 2
    assert len(bundle.historical_case_evidence) == 1
    assert len(bundle.policy_evidence) == 1

    historical_evidence = bundle.historical_case_evidence[0]

    assert historical_evidence.source_id == "CASE-001"
    assert historical_evidence.source_type == "historical_fraud_case"
    assert historical_evidence.score == historical_result.score
    assert historical_evidence.metadata["chunk_id"] == 101
    assert historical_evidence.metadata["semantic_score"] == 0.90
    assert historical_evidence.metadata["keyword_score"] == 0.80

    policy_evidence = bundle.policy_evidence[0]

    assert policy_evidence.source_id == "POLICY-AML-001"
    assert policy_evidence.source_type == "aml_policy"
    assert policy_evidence.score == policy_result.score
    assert policy_evidence.metadata["chunk_id"] == 201


def test_existing_transaction_evidence_is_preserved(
    db: Session,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "api.services.evidence.hybrid_search",
        Mock(return_value=[]),
    )
    
    context = build_investigation_context(
        db,
        "ALERT-001",
    )
    
    assert context is not None
    
    bundle = build_evidence_bundle(db, context)

    assert len(bundle.transaction_evidence) == 2

    assert [
        evidence.source_id
        for evidence in bundle.transaction_evidence
    ] == [
        "ALERT-001",
        "TXN-004",
    ]