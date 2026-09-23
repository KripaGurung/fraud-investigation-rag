from api.investigation.evaluation.semantic_evaluator import (
    FindingSemanticEvaluation,
    evaluate_case_semantic_groundedness,
    evaluate_finding_semantic_groundedness,
)
from api.investigation.evaluation.semantic_groundedness import (
    SemanticGroundednessResult,
)
from api.investigation.context import build_investigation_context

from api.investigation.generation.schemas import (
    InvestigationCase,
    InvestigationFinding,
)
from tests.fixtures.evidence_bundles import clearly_suspicious_bundle


class FakeSemanticEvaluator:
    def __init__(self, result: SemanticGroundednessResult) -> None:
        self.result = result
        self.received_statement = None
        self.received_evidence_contents = None

    def evaluate(
        self,
        statement: str,
        evidence_contents: list[str],
    ) -> SemanticGroundednessResult:
        self.received_statement = statement
        self.received_evidence_contents = evidence_contents
        return self.result

def test_evaluate_finding_resolves_cited_evidence_content():
    expected_result = SemanticGroundednessResult(
        is_supported=True,
        explanation="The cited evidence supports the finding.",
    )
    evaluator = FakeSemanticEvaluator(expected_result)

    result = evaluate_finding_semantic_groundedness(
        statement="The transaction amount was unusually high.",
        evidence_ids=["TXN-001", "CASE-001"],
        evidence_content_map={
            "TXN-001": "Transaction amount was $5,000.",
            "CASE-001": "Previous case involved unusual activity.",
        },
        evaluator=evaluator,
    )

    assert isinstance(result, FindingSemanticEvaluation)
    assert result.statement == "The transaction amount was unusually high."
    assert result.evidence_ids == ["TXN-001", "CASE-001"]
    assert result.result is expected_result

    assert evaluator.received_statement == (
        "The transaction amount was unusually high."
    )
    assert evaluator.received_evidence_contents == [
        "Transaction amount was $5,000.",
        "Previous case involved unusual activity.",
    ]    

def test_evaluate_finding_ignores_unknown_evidence_ids():
    expected_result = SemanticGroundednessResult(
        is_supported=False,
        explanation="The available evidence is insufficient.",
    )
    evaluator = FakeSemanticEvaluator(expected_result)

    result = evaluate_finding_semantic_groundedness(
        statement="The transaction is suspicious.",
        evidence_ids=["TXN-001", "FAKE-999"],
        evidence_content_map={
            "TXN-001": "Transaction was made outside the customer's usual pattern.",
        },
        evaluator=evaluator,
    )

    assert result.evidence_ids == ["TXN-001", "FAKE-999"]
    assert result.result is expected_result

    assert evaluator.received_evidence_contents == [
        "Transaction was made outside the customer's usual pattern.",
    ]    

def test_evaluate_case_evaluates_all_findings():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    evidence_ids = [
        analyzed.evidence.source_id
        for analyzed in context.analyzed_evidence[:2]
    ]

    evaluator = FakeSemanticEvaluator(
        SemanticGroundednessResult(
            is_supported=True,
            explanation="The cited evidence supports the finding.",
        )
    )

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test risk narrative.",
        supporting_findings=[
            InvestigationFinding(
                statement="Supporting finding.",
                evidence_ids=[evidence_ids[0]],
            )
        ],
        contradicting_findings=[
            InvestigationFinding(
                statement="Contradicting finding.",
                evidence_ids=[evidence_ids[1]],
            )
        ],
    )

    results = evaluate_case_semantic_groundedness(
        case,
        context,
        evaluator,
    )

    assert len(results) == 2

    assert results[0].statement == "Supporting finding."
    assert results[0].evidence_ids == [evidence_ids[0]]
    assert results[0].result.is_supported is True

    assert results[1].statement == "Contradicting finding."
    assert results[1].evidence_ids == [evidence_ids[1]]
    assert results[1].result.is_supported is True    