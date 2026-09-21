from sqlalchemy.orm import Session

from api.repositories.fraud_alert import (
    get_customer_transaction_history,
    get_fraud_alert,
)


def test_get_fraud_alert(db: Session) -> None:
    alert = get_fraud_alert(db, "ALERT-001")

    assert alert is not None
    assert alert.alert_reference == "ALERT-001"
    assert alert.transaction is not None
    assert alert.transaction.transaction_reference == "TXN-004"
    assert alert.transaction.amount == 450000


def test_get_fraud_alert_returns_none_for_unknown_alert(
    db: Session,
) -> None:
    alert = get_fraud_alert(db, "ALERT-DOES-NOT-EXIST")

    assert alert is None


def test_get_customer_transaction_history(db: Session) -> None:
    alert = get_fraud_alert(db, "ALERT-001")

    assert alert is not None
    assert alert.transaction is not None

    history = get_customer_transaction_history(
        db,
        account_id=alert.transaction.account_id,
        before_transaction_id=alert.transaction.id,
    )

    assert [transaction.transaction_reference for transaction in history] == [
        "TXN-003",
        "TXN-002",
        "TXN-001",
    ]


def test_customer_transaction_history_excludes_alerted_transaction(
    db: Session,
) -> None:
    alert = get_fraud_alert(db, "ALERT-001")

    assert alert is not None
    assert alert.transaction is not None

    history = get_customer_transaction_history(
        db,
        account_id=alert.transaction.account_id,
        before_transaction_id=alert.transaction.id,
    )

    assert all(
        transaction.id != alert.transaction.id
        for transaction in history
    )