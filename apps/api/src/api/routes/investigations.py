from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.core.config import settings
from api.db.session import get_db
from api.investigation.generation.generator import GeminiReportGenerator
from api.investigation.generation.openai_generator import (
    OpenAIInvestigationGenerator,
)
from api.investigation.generation.schemas import InvestigationCase
from api.schemas.investigation import InvestigationResult
from api.schemas.investigation_evidence import (
    InvestigationEvidenceResponse,
)
from api.services.generation import generate_investigation
from api.services.investigation_evidence import (
    get_investigation_evidence,
)
from api.services.investigation_pipeline import run_investigation


router = APIRouter(
    tags=["investigations"],
)

legacy_router = APIRouter(
    prefix="/investigations",
)

api_v1_router = APIRouter(
    prefix="/api/v1/investigations",
)


def get_investigation_generator_factory() -> (
    Callable[[], OpenAIInvestigationGenerator]
):
    """Provide a factory for the configured investigation generator."""

    def factory() -> OpenAIInvestigationGenerator:
        try:
            return OpenAIInvestigationGenerator()
        except ValueError as exc:
            raise HTTPException(
                status_code=503,
                detail=str(exc),
            ) from exc

    return factory


def get_report_generator() -> GeminiReportGenerator:
    return GeminiReportGenerator(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
    )


@legacy_router.post(
    "/{alert_reference}/generate",
    response_model=InvestigationCase,
)
def generate_investigation_case(
    alert_reference: str,
    db: Session = Depends(get_db),
    generator_factory: Callable[
        [], OpenAIInvestigationGenerator
    ] = Depends(get_investigation_generator_factory),
) -> InvestigationCase:
    """Generate an investigator-ready case for a fraud alert."""
    try:
        result = generate_investigation(
            db,
            alert_reference,
            generator_factory,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Fraud alert '{alert_reference}' was not found.",
        )

    return result


@legacy_router.get(
    "/{alert_reference}/evidence",
    response_model=InvestigationEvidenceResponse,
)
def get_investigation_evidence_route(
    alert_reference: str,
    db: Session = Depends(get_db),
) -> InvestigationEvidenceResponse:
    """Return analyzed evidence for a fraud investigation."""
    result = get_investigation_evidence(
        db,
        alert_reference,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Fraud alert '{alert_reference}' was not found.",
        )

    return result


@api_v1_router.post(
    "/{alert_reference}",
    response_model=InvestigationResult,
)
def investigate_alert(
    alert_reference: str,
    db: Session = Depends(get_db),
    report_generator: GeminiReportGenerator = Depends(get_report_generator),
) -> InvestigationResult:
    result = run_investigation(
        db,
        alert_reference,
        report_generator=report_generator,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fraud alert '{alert_reference}' was not found.",
        )

    return result


router.include_router(legacy_router)
router.include_router(api_v1_router)