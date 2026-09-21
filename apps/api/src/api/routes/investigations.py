from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.schemas.investigation import InvestigationResult
from api.services.investigation_pipeline import run_investigation


router = APIRouter(
    prefix="/api/v1/investigations",
    tags=["investigations"],
)


@router.post(
    "/{alert_reference}",
    response_model=InvestigationResult,
)
def investigate_alert(
    alert_reference: str,
    db: Session = Depends(get_db),
) -> InvestigationResult:
    result = run_investigation(
        db,
        alert_reference,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fraud alert '{alert_reference}' was not found.",
        )

    return result