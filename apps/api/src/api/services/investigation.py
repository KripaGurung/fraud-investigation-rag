from dataclasses import dataclass

from sqlalchemy.orm import Session

from api.models import Account, Customer, FraudAlert, Transaction
from api.repositories.fraud_alert import (
    get_customer_transaction_history,
    get_fraud_alert,
)


@dataclass
class InvestigationContext:
    alert: FraudAlert
    transaction: Transaction
    account: Account
    customer: Customer
    historical_transactions: list[Transaction]


def build_investigation_context(
    db: Session,
    alert_reference: str,
) -> InvestigationContext | None:
    alert = get_fraud_alert(db, alert_reference)

    if alert is None:
        return None

    transaction = alert.transaction
    account = transaction.account
    customer = account.customer

    historical_transactions = get_customer_transaction_history(
        db,
        account_id=account.id,
        before_transaction_id=transaction.id,
    )

    return InvestigationContext(
        alert=alert,
        transaction=transaction,
        account=account,
        customer=customer,
        historical_transactions=historical_transactions,
    )