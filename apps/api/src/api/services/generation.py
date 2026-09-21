from collections.abc import Callable

from sqlalchemy.orm import Session

from api.investigation.context import (
    build_investigation_context as build_intelligence_context,
)
from api.investigation.generation.generator import InvestigationGenerator
from api.investigation.generation.schemas import InvestigationCase
from api.services.evidence import build_evidence_bundle
from api.services.investigation import build_investigation_context


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

    return generator.generate(
        alert_reference,
        intelligence_context,
    )