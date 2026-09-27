from sqlalchemy.orm import Session

from api.investigation.context import (
    build_investigation_context as build_analysis_context,
)
from api.schemas.investigation_evidence import (
    InvestigationEvidenceResponse,
)
from api.services.evidence import build_evidence_bundle
from api.services.investigation import (
    build_investigation_context as build_database_context,
)


def get_investigation_evidence(
    db: Session,
    alert_reference: str,
) -> InvestigationEvidenceResponse | None:
    """Build analyzed evidence for a fraud investigation."""
    database_context = build_database_context(
        db,
        alert_reference,
    )

    if database_context is None:
        return None

    evidence_bundle = build_evidence_bundle(database_context)
    analysis_context = build_analysis_context(evidence_bundle)

    return InvestigationEvidenceResponse(
        alert_id=evidence_bundle.alert_id,
        analyzed_evidence=analysis_context.analyzed_evidence,
        missing_evidence=analysis_context.missing_evidence,
    )