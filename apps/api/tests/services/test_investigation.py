from sqlalchemy.orm import Session

from api.services.investigation import (
    InvestigationContext,
    build_investigation_context,
)


def test_build_investigation_context(db: Session) -> None:
    context = build_investigation_context(db, "ALERT-001")

    assert context is not None
    assert isinstance(context, InvestigationContext)

    assert context.alert.alert_reference == "ALERT-001"
    assert context.transaction.transaction_reference == "TXN-004"
    assert context.account.account_number == "ACC-001"
    assert context.customer.customer_number == "CUST-001"
    assert context.customer.full_name == "Maya Sharma"

    assert [
        transaction.transaction_reference
        for transaction in context.historical_transactions
    ] == [
        "TXN-003",
        "TXN-002",
        "TXN-001",
    ]


def test_build_investigation_context_returns_none_for_unknown_alert(
    db: Session,
) -> None:
    context = build_investigation_context(
        db,
        "ALERT-DOES-NOT-EXIST",
    )

    assert context is None


def test_investigation_context_contains_alerted_transaction(
    db: Session,
) -> None:
    context = build_investigation_context(db, "ALERT-001")

    assert context is not None
    assert context.transaction.transaction_reference == "TXN-004"
    assert context.transaction.amount == 450000


def test_investigation_context_history_excludes_alerted_transaction(
    db: Session,
) -> None:
    context = build_investigation_context(db, "ALERT-001")

    assert context is not None

    history_references = [
        transaction.transaction_reference
        for transaction in context.historical_transactions
    ]

    assert "TXN-004" not in history_references