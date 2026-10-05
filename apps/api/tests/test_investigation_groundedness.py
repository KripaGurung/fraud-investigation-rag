from api.investigation.context import build_investigation_context
from api.investigation.evaluation.groundedness import evaluate_groundedness
from api.investigation.generation.schemas import (
    InvestigationCase,
    InvestigationFinding,
)
from tests.fixtures.evidence_bundles import clearly_suspicious_bundle


def test_valid_citations_are_fully_grounded():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    evidence_id = context.analyzed_evidence[0].evidence.source_id

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test risk narrative.",
        supporting_findings=[
            InvestigationFinding(
                statement="Suspicious activity requires investigation.",
                evidence_ids=[evidence_id],
            )
        ],
    )

    result = evaluate_groundedness(case, context)

    assert result.score == 1.0
    assert result.total_findings == 1
    assert result.grounded_findings == 1
    assert result.ungrounded_findings == [] 

def test_unknown_citation_is_ungrounded():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test risk narrative.",
        supporting_findings=[
            InvestigationFinding(
                statement="Finding based on unavailable evidence.",
                evidence_ids=["FAKE-999"],
            )
        ],
    )

    result = evaluate_groundedness(case, context)

    assert result.score == 0.0
    assert result.total_findings == 1
    assert result.grounded_findings == 0
    assert result.ungrounded_findings == [
        "Finding based on unavailable evidence."
    ] 

def test_uncited_finding_is_ungrounded():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test risk narrative.",
        supporting_findings=[
            InvestigationFinding(
                statement="Finding without evidence citations.",
                evidence_ids=[],
            )
        ],
    )

    result = evaluate_groundedness(case, context)

    assert result.score == 0.0
    assert result.total_findings == 1
    assert result.grounded_findings == 0
    assert result.ungrounded_findings == [
        "Finding without evidence citations."
    ]   

def test_mixed_findings_produce_partial_groundedness_score():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    evidence_id = context.analyzed_evidence[0].evidence.source_id

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test risk narrative.",
        supporting_findings=[
            InvestigationFinding(
                statement="Grounded finding.",
                evidence_ids=[evidence_id],
            ),
            InvestigationFinding(
                statement="Ungrounded finding.",
                evidence_ids=["FAKE-999"],
            ),
        ],
    )

    result = evaluate_groundedness(case, context)

    assert result.score == 0.5
    assert result.total_findings == 2
    assert result.grounded_findings == 1
    assert result.ungrounded_findings == [
        "Ungrounded finding."
    ]        

def test_report_without_findings_has_full_groundedness():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test risk narrative.",
    )

    result = evaluate_groundedness(case, context)

    assert result.score == 1.0
    assert result.total_findings == 0
    assert result.grounded_findings == 0
    assert result.ungrounded_findings == []    