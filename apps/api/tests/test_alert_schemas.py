from datetime import datetime, timezone
from types import SimpleNamespace

from api.schemas.alerts import (
    AccountDetail,
    CustomerDetail,
    FraudAlertDetail,
    FraudAlertSummary,
    TransactionDetail,
)


def test_fraud_alert_summary_builds_from_attributes() -> None:
    alert = SimpleNamespace(
        alert_reference="ALERT-001",
        alert_type="high_value_transaction",
        severity="high",
        status="open",
        reason="Transaction amount exceeded expected activity.",
        triggered_at=datetime(
            2026,
            1,
            1,
            12,
            0,
            tzinfo=timezone.utc,
        ),
    )

    summary = FraudAlertSummary.model_validate(alert)

    assert summary.alert_reference == "ALERT-001"
    assert summary.alert_type == "high_value_transaction"
    assert summary.severity == "high"
    assert summary.status == "open"
    assert summary.reason == (
        "Transaction amount exceeded expected activity."
    )
    assert summary.triggered_at == alert.triggered_at

def test_transaction_detail_builds_from_attributes() -> None:
    transaction = SimpleNamespace(
        transaction_reference="TXN-001",
        amount="15000.00",
        currency="USD",
        transaction_type="transfer",
        direction="outbound",
        counterparty_account="ACC-999",
        counterparty_name="Example Counterparty",
        country="US",
        city="New York",
        device_id="DEVICE-001",
        ip_address="192.0.2.1",
        channel="online",
        status="completed",
        occurred_at=datetime(
            2026,
            1,
            1,
            11,
            30,
            tzinfo=timezone.utc,
        ),
    )

    detail = TransactionDetail.model_validate(transaction)

    assert detail.transaction_reference == "TXN-001"
    assert detail.currency == "USD"
    assert detail.transaction_type == "transfer"
    assert detail.direction == "outbound"
    assert detail.counterparty_name == "Example Counterparty"
    assert detail.channel == "online"    

def test_account_detail_builds_from_attributes() -> None:
    account = SimpleNamespace(
        account_number="ACC-001",
        account_type="checking",
        currency="USD",
        status="active",
        current_balance="25000.00",
        opened_at=datetime(
            2024,
            1,
            1,
            10,
            0,
            tzinfo=timezone.utc,
        ),
    )

    detail = AccountDetail.model_validate(account)

    assert detail.account_number == "ACC-001"
    assert detail.account_type == "checking"
    assert detail.currency == "USD"
    assert detail.status == "active"   

def test_customer_detail_builds_from_attributes() -> None:
    customer = SimpleNamespace(
        customer_number="CUST-001",
        full_name="Example Customer",
        country="US",
        risk_level="high",
        kyc_status="verified",
    )

    detail = CustomerDetail.model_validate(customer)

    assert detail.customer_number == "CUST-001"
    assert detail.full_name == "Example Customer"
    assert detail.country == "US"
    assert detail.risk_level == "high"
    assert detail.kyc_status == "verified"     

def test_fraud_alert_detail_combines_investigation_context() -> None:
    detail = FraudAlertDetail(
        alert_reference="ALERT-001",
        alert_type="high_value_transaction",
        severity="high",
        status="open",
        reason="Transaction amount exceeded expected activity.",
        triggered_at=datetime(
            2026,
            1,
            1,
            12,
            0,
            tzinfo=timezone.utc,
        ),
        transaction=TransactionDetail(
            transaction_reference="TXN-001",
            amount="15000.00",
            currency="USD",
            transaction_type="transfer",
            direction="outbound",
            counterparty_account="ACC-999",
            counterparty_name="Example Counterparty",
            country="US",
            city="New York",
            device_id="DEVICE-001",
            ip_address="192.0.2.1",
            channel="online",
            status="completed",
            occurred_at=datetime(
                2026,
                1,
                1,
                11,
                30,
                tzinfo=timezone.utc,
            ),
        ),
        account=AccountDetail(
            account_number="ACC-001",
            account_type="checking",
            currency="USD",
            status="active",
            current_balance="25000.00",
            opened_at=datetime(
                2024,
                1,
                1,
                10,
                0,
                tzinfo=timezone.utc,
            ),
        ),
        customer=CustomerDetail(
            customer_number="CUST-001",
            full_name="Example Customer",
            country="US",
            risk_level="high",
            kyc_status="verified",
        ),
    )

    assert detail.alert_reference == "ALERT-001"
    assert detail.transaction.transaction_reference == "TXN-001"
    assert detail.account.account_number == "ACC-001"
    assert detail.customer.customer_number == "CUST-001"    