from api.investigation.generation.schemas import (
    InvestigationCase,
    InvestigationFinding,
)


def test_investigation_case_preserves_evidence_references() -> None:
    finding = InvestigationFinding(
        statement="The transaction is inconsistent with prior customer activity.",
        evidence_ids=["txn-001", "case-001"],
    )

    case = InvestigationCase(
        alert_id="ALERT-001",
        executive_summary="The alert requires further investigation.",
        risk_narrative="Multiple pieces of evidence indicate unusual activity.",
        supporting_findings=[finding],
        missing_evidence=["policy_evidence"],
        recommended_follow_up=["Review the beneficiary relationship."],
    )

    assert case.alert_id == "ALERT-001"
    assert case.supporting_findings[0].statement == (
        "The transaction is inconsistent with prior customer activity."
    )
    assert case.supporting_findings[0].evidence_ids == [
        "txn-001",
        "case-001",
    ]