from sqlalchemy.orm import Session

from api.investigation.context import (
    build_investigation_context as build_analysis_context,
)
from api.investigation.generation.generator import (
    DeterministicReportGenerator,
    InvestigationReportGenerator,
)
from api.investigation.generation.prompt import (
    SYSTEM_PROMPT,
    build_investigation_prompt,
)
from api.investigation.schemas import EvidenceClassification
from api.schemas.investigation import InvestigationResult
from api.services.evidence import build_evidence_bundle
from api.services.investigation import build_investigation_context


def run_investigation(
    db: Session,
    alert_reference: str,
    report_generator: InvestigationReportGenerator | None = None,
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

    investigation_prompt = build_investigation_prompt(
        analysis_context,
    )

    generator = report_generator or DeterministicReportGenerator()

    report = generator.generate(
        SYSTEM_PROMPT,
        investigation_prompt,
    )

    return InvestigationResult(
        alert_id=evidence_bundle.alert_id,
        supporting_evidence=supporting_evidence,
        contradicting_evidence=contradicting_evidence,
        missing_evidence=analysis_context.missing_evidence,
        summary=summary,
        report=report,
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