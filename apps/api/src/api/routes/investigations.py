from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.investigation.generation.openai_generator import (
    OpenAIInvestigationGenerator,
)
from api.investigation.generation.schemas import InvestigationCase
from api.services.generation import generate_investigation

from collections.abc import Callable


router = APIRouter(
    prefix="/investigations",
    tags=["investigations"],
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


@router.post(
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