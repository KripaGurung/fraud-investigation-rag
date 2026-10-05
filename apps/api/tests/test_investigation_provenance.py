from api.investigation.context import build_investigation_context
from api.investigation.generation.provenance import (
    validate_case_provenance,
    validate_evidence_citations,
)
from api.investigation.generation.schemas import (
    InvestigationCase,
    InvestigationFinding,
)

from tests.fixtures.evidence_bundles import clearly_suspicious_bundle


def test_validate_evidence_citations_accepts_known_evidence_ids():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    known_evidence_id = context.analyzed_evidence[0].evidence.source_id

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test narrative.",
        supporting_findings=[
            InvestigationFinding(
                statement="Suspicious activity requires investigation.",
                evidence_ids=[known_evidence_id],
            )
        ],
    )

    invalid_ids = validate_evidence_citations(
        case,
        context,
    )

    assert invalid_ids == []

def test_validate_evidence_citations_detects_unknown_evidence_ids():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test narrative.",
        supporting_findings=[
            InvestigationFinding(
                statement="Unsupported generated finding.",
                evidence_ids=["FAKE-999"],
            )
        ],
    )

    invalid_ids = validate_evidence_citations(
        case,
        context,
    )

    assert invalid_ids == ["FAKE-999"]    

def test_validate_evidence_citations_checks_contradicting_findings():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test narrative.",
        contradicting_findings=[
            InvestigationFinding(
                statement="Generated contradictory finding.",
                evidence_ids=["UNKNOWN-CONTRADICTION-001"],
            )
        ],
    )

    invalid_ids = validate_evidence_citations(
        case,
        context,
    )

    assert invalid_ids == ["UNKNOWN-CONTRADICTION-001"]    
def test_validate_evidence_citations_detects_uncited_findings():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test narrative.",
        supporting_findings=[
            InvestigationFinding(
                statement="Finding without supporting provenance.",
                evidence_ids=[],
            )
        ],
    )

    invalid_ids = validate_evidence_citations(
        case,
        context,
    )

    assert invalid_ids == []

def test_validate_case_provenance_reports_uncited_findings():
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test narrative.",
        supporting_findings=[
            InvestigationFinding(
                statement="Finding without supporting provenance.",
                evidence_ids=[],
            )
        ],
    )

    result = validate_case_provenance(
        case,
        context,
    )

    assert result.invalid_evidence_ids == []
    assert result.uncited_findings == [
        "Finding without supporting provenance."
    ]  