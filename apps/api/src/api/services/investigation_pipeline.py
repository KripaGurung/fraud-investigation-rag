from sqlalchemy.orm import Session

from api.schemas.investigation import InvestigationResult
from api.services.evidence import build_evidence_bundle
from api.services.investigation import build_investigation_context
from api.investigation.context import (
    build_investigation_context as build_analysis_context,
)
from api.investigation.schemas import EvidenceClassification


def run_investigation(
    db: Session,
    alert_reference: str,
) -> InvestigationResult | None:
    investigation_context = build_investigation_context(
        db,
        alert_reference,
    )

    if investigation_context is None:
        return None

    evidence_bundle = build_evidence_bundle(
        db,
        investigation_context,
    )

    analysis_context = build_analysis_context(
        evidence_bundle,
    )

    supporting_evidence = [
        item.evidence
        for item in analysis_context.analyzed_evidence
        if item.classification == EvidenceClassification.SUPPORTING
    ]

    contradicting_evidence = [
        item.evidence
        for item in analysis_context.analyzed_evidence
        if item.classification == EvidenceClassification.CONTRADICTING
    ]

    summary = _build_summary(
        supporting_count=len(supporting_evidence),
        contradicting_count=len(contradicting_evidence),
        missing_evidence=analysis_context.missing_evidence,
    )

    return InvestigationResult(
        alert_id=evidence_bundle.alert_id,
        supporting_evidence=supporting_evidence,
        contradicting_evidence=contradicting_evidence,
        missing_evidence=analysis_context.missing_evidence,
        summary=summary,
    )


def _build_summary(
    supporting_count: int,
    contradicting_count: int,
    missing_evidence: list[str],
) -> str:
    parts = [
        (
            f"Investigation identified {supporting_count} "
            "supporting evidence item(s)"
        ),
        (
            f"{contradicting_count} contradicting evidence item(s)"
        ),
    ]

    if missing_evidence:
        parts.append(
            "Missing evidence categories: "
            + ", ".join(missing_evidence)
            + "."
        )
    else:
        parts.append("No required evidence categories are missing.")

    return ". ".join(parts)