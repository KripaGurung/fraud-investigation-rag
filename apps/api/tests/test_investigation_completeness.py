from api.investigation.evaluation.completeness import (
    evaluate_report_completeness,
)
from api.investigation.generation.schemas import (
    InvestigationCase,
    InvestigationFinding,
)


def test_complete_report_is_marked_complete():
    case = InvestigationCase(
        alert_id="ALERT-001",
        executive_summary="Suspicious transaction activity requires review.",
        risk_narrative="The transaction differs from observed account activity.",
        supporting_findings=[
            InvestigationFinding(
                statement="The transaction shows suspicious characteristics.",
                evidence_ids=["txn-001"],
            )
        ],
    )

    result = evaluate_report_completeness(case)

    assert result.is_complete is True
    assert result.missing_sections == []

def test_incomplete_report_identifies_missing_sections():
    case = InvestigationCase(
        alert_id="ALERT-001",
        executive_summary="",
        risk_narrative="",
        supporting_findings=[],
    )

    result = evaluate_report_completeness(case)

    assert result.is_complete is False
    assert result.missing_sections == [
        "executive_summary",
        "risk_narrative",
        "supporting_findings",
    ] 

def test_whitespace_only_text_sections_are_incomplete():
    case = InvestigationCase(
        alert_id="ALERT-001",
        executive_summary="   ",
        risk_narrative="   ",
        supporting_findings=[
            InvestigationFinding(
                statement="Suspicious activity requires review.",
                evidence_ids=["txn-001"],
            )
        ],
    )

    result = evaluate_report_completeness(case)

    assert result.is_complete is False
    assert result.missing_sections == [
        "executive_summary",
        "risk_narrative",
    ]       