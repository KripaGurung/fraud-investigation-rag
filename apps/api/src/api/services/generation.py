from collections.abc import Callable

from sqlalchemy.orm import Session

from api.investigation.context import (
    build_investigation_context as build_intelligence_context,
)
from api.investigation.generation.generator import InvestigationGenerator
from api.investigation.generation.schemas import InvestigationCase
from api.services.evidence import build_evidence_bundle
from api.services.investigation import build_investigation_context
from api.investigation.generation.provenance import (
    validate_case_provenance,
)


def generate_investigation(
    db: Session,
    alert_reference: str,
    generator_factory: Callable[[], InvestigationGenerator],
) -> InvestigationCase | None:
    """Build evidence context and generate an investigator-ready case."""
    investigation_context = build_investigation_context(
        db,
        alert_reference,
    )

    if investigation_context is None:
        return None

    evidence_bundle = build_evidence_bundle(investigation_context)

    intelligence_context = build_intelligence_context(
        evidence_bundle,
    )

    generator = generator_factory()

    case = generator.generate(
       alert_reference,
       intelligence_context,
    )

    validation = validate_case_provenance(
        case,
        intelligence_context,
    )

    if validation.invalid_evidence_ids:
        raise ValueError(
            "Generated investigation contains invalid evidence citations: "
            + ", ".join(validation.invalid_evidence_ids)
        )

    if validation.uncited_findings:
        raise ValueError(
            "Generated investigation contains uncited findings: "
            + "; ".join(validation.uncited_findings)
        )

    return case