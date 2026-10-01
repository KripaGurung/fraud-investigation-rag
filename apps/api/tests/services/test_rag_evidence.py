from unittest.mock import Mock

from sqlalchemy.orm import Session

from api.rag.retrieval.hybrid import HybridSearchResult
from api.rag.retrieval.reranker import RerankedSearchResult
from api.schemas.evidence import EvidenceBundle
from api.services.evidence import build_evidence_bundle
from api.services.investigation import build_investigation_context


def test_evidence_bundle_includes_reranked_rag_evidence(
    db: Session,
    monkeypatch,
) -> None:
    historical_candidate = HybridSearchResult(
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

    policy_candidate = HybridSearchResult(
        chunk_id=201,
        document_reference="POLICY-AML-001",
        document_type="aml_policy",
        title="Monitoring Significant Deviations from Customer Transaction Patterns",
        source="synthetic_aml_policy_corpus",
        chunk_index=0,
        content=(
            "Significant deviations from established transaction patterns "
            "may warrant review."
        ),
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
            return [historical_candidate]

        if document_type == "aml_policy":
            return [policy_candidate]

        return []

    def mock_rerank_results(
        query,
        results,
        limit,
    ):
        return [
            RerankedSearchResult(
                chunk_id=result.chunk_id,
                document_reference=result.document_reference,
                document_type=result.document_type,
                title=result.title,
                source=result.source,
                chunk_index=result.chunk_index,
                content=result.content,
                semantic_score=result.semantic_score,
                keyword_score=result.keyword_score,
                hybrid_score=result.score,
                rerank_score=0.95,
                score=0.95,
            )
            for result in results[:limit]
        ]

    monkeypatch.setattr(
        "api.services.evidence.hybrid_search",
        mock_hybrid_search,
    )

    monkeypatch.setattr(
        "api.services.evidence.rerank_results",
        mock_rerank_results,
        raising=False,
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
    assert historical_evidence.score == 0.95
    assert historical_evidence.metadata["chunk_id"] == 101
    assert historical_evidence.metadata["semantic_score"] == 0.90
    assert historical_evidence.metadata["keyword_score"] == 0.80
    assert historical_evidence.metadata["hybrid_score"] == 0.87
    assert historical_evidence.metadata["rerank_score"] == 0.95

    policy_evidence = bundle.policy_evidence[0]

    assert policy_evidence.source_id == "POLICY-AML-001"
    assert policy_evidence.source_type == "aml_policy"
    assert policy_evidence.score == 0.95
    assert policy_evidence.metadata["chunk_id"] == 201
    assert policy_evidence.metadata["hybrid_score"] == 0.841
    assert policy_evidence.metadata["rerank_score"] == 0.95


def test_existing_transaction_evidence_is_preserved(
    db: Session,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "api.services.evidence.hybrid_search",
        Mock(return_value=[]),
    )

    monkeypatch.setattr(
        "api.services.evidence.rerank_results",
        Mock(return_value=[]),
        raising=False,
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