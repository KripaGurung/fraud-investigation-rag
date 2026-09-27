from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.repositories.fraud_alert import (
    get_fraud_alert,
    list_fraud_alerts,
)
from api.schemas.alerts import (
    AccountDetail,
    CustomerDetail,
    FraudAlertDetail,
    FraudAlertSummary,
    TransactionDetail,
)


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

@router.get(
    "/{alert_reference}",
    response_model=FraudAlertDetail,
)
def get_alert_detail(
    alert_reference: str,
    db: Session = Depends(get_db),
) -> FraudAlertDetail:
    """Return investigator-facing details for one fraud alert."""
    alert = get_fraud_alert(db, alert_reference)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail=f"Fraud alert '{alert_reference}' was not found.",
        )

    transaction = alert.transaction
    account = transaction.account
    customer = account.customer

    return FraudAlertDetail(
        alert_reference=alert.alert_reference,
        alert_type=alert.alert_type,
        severity=alert.severity,
        status=alert.status,
        reason=alert.reason,
        triggered_at=alert.triggered_at,
        transaction=TransactionDetail.model_validate(transaction),
        account=AccountDetail.model_validate(account),
        customer=CustomerDetail.model_validate(customer),
    )