from api.investigation.context import build_investigation_context
from api.investigation.evaluation.evaluator import evaluate_investigation
from api.investigation.generation.schemas import (
    InvestigationCase,
    InvestigationFinding,
)
from api.investigation.evaluation.semantic_groundedness import (
    SemanticGroundednessResult,
)
from tests.fixtures.evidence_bundles import clearly_suspicious_bundle


class FakeSemanticEvaluator:
    def evaluate(
        self,
        statement: str,
        evidence_contents: list[str],
    ) -> SemanticGroundednessResult:
        return SemanticGroundednessResult(
            is_supported=True,
            explanation="The cited evidence supports the finding.",
        )
    
def test_evaluate_investigation_combines_evaluation_results():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    evidence_id = context.analyzed_evidence[0].evidence.source_id

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Suspicious transaction activity requires review.",
        risk_narrative="The transaction differs from observed activity.",
        supporting_findings=[
            InvestigationFinding(
                statement="Suspicious activity requires investigation.",
                evidence_ids=[evidence_id],
            )
        ],
    )

    result = evaluate_investigation(case, context)

    assert result.completeness.is_complete is True
    assert result.completeness.missing_sections == []

    assert result.groundedness.score == 1.0
    assert result.groundedness.total_findings == 1
    assert result.groundedness.grounded_findings == 1
    assert result.groundedness.ungrounded_findings == []
    assert result.semantic_groundedness is None

def test_evaluate_investigation_preserves_evaluation_failures():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="",
        risk_narrative="",
        supporting_findings=[
            InvestigationFinding(
                statement="Finding based on unavailable evidence.",
                evidence_ids=["FAKE-999"],
            )
        ],
    )

    result = evaluate_investigation(case, context)

    assert result.completeness.is_complete is False
    assert result.completeness.missing_sections == [
        "executive_summary",
        "risk_narrative",
    ]

    assert result.groundedness.score == 0.0
    assert result.groundedness.total_findings == 1
    assert result.groundedness.grounded_findings == 0
    assert result.groundedness.ungrounded_findings == [
        "Finding based on unavailable evidence."
    ]  

def test_evaluate_investigation_includes_semantic_groundedness_when_enabled():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    evidence_id = context.analyzed_evidence[0].evidence.source_id

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Suspicious transaction activity requires review.",
        risk_narrative="The transaction differs from observed activity.",
        supporting_findings=[
            InvestigationFinding(
                statement="Suspicious activity requires investigation.",
                evidence_ids=[evidence_id],
            )
        ],
    )

    result = evaluate_investigation(
        case,
        context,
        semantic_evaluator=FakeSemanticEvaluator(),
    )

    assert result.semantic_groundedness is not None
    assert result.semantic_groundedness.score == 1.0
    assert result.semantic_groundedness.total_findings == 1
    assert result.semantic_groundedness.supported_findings == 1
    assert result.semantic_groundedness.unsupported_findings == []

    assert len(result.semantic_groundedness.finding_evaluations) == 1

    finding_evaluation = result.semantic_groundedness.finding_evaluations[0]

    assert finding_evaluation.statement == (
        "Suspicious activity requires investigation."
    )
    assert finding_evaluation.evidence_ids == [evidence_id]
    assert finding_evaluation.result.is_supported is True