from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.repositories.fraud_alert import list_fraud_alerts
from api.schemas.alerts import FraudAlertSummary


router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
)


@router.get(
    "",
    response_model=list[FraudAlertSummary],
)
def get_alerts(
    db: Session = Depends(get_db),
) -> list[FraudAlertSummary]:
    """Return fraud alerts available for investigation."""
    return list_fraud_alerts(db)