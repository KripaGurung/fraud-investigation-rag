from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from api.models import Account, FraudAlert, Transaction


def get_fraud_alert(
    db: Session,
    alert_reference: str,
) -> FraudAlert | None:
    statement = (
        select(FraudAlert)
        .options(
            joinedload(FraudAlert.transaction)
            .joinedload(Transaction.account)
            .joinedload(Account.customer),
        )
        .where(FraudAlert.alert_reference == alert_reference)
    )

    return db.scalar(statement)

def list_fraud_alerts(
    db: Session,
) -> list[FraudAlert]:
    """Return available fraud alerts."""
    statement = select(FraudAlert)

    return list(db.scalars(statement).all())


def get_customer_transaction_history(
    db: Session,
    account_id: int,
    before_transaction_id: int,
) -> list[Transaction]:
    statement = (
        select(Transaction)
        .where(
            Transaction.account_id == account_id,
            Transaction.id < before_transaction_id,
        )
        .order_by(Transaction.occurred_at.desc())
    )

    return list(db.scalars(statement).all())