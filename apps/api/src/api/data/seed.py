from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select

from api.db.session import SessionLocal
from api.models import Account, Customer, FraudAlert, Transaction


def seed_financial_data() -> None:
    db = SessionLocal()

    try:
        existing_customer = db.scalar(
            select(Customer).where(Customer.customer_number == "CUST-001")
        )

        if existing_customer is not None:
            print("Synthetic financial data already exists. Skipping seed.")
            return

        customer = Customer(
            customer_number="CUST-001",
            full_name="Maya Sharma",
            country="NP",
            risk_level="medium",
            kyc_status="verified",
        )

        account = Account(
            account_number="ACC-001",
            customer=customer,
            account_type="checking",
            currency="NPR",
            status="active",
            current_balance=Decimal("750000.00"),
            opened_at=datetime(
                2024,
                1,
                15,
                9,
                0,
                tzinfo=timezone.utc,
            ),
        )

        normal_transaction_1 = Transaction(
            transaction_reference="TXN-001",
            account=account,
            amount=Decimal("4500.00"),
            currency="NPR",
            transaction_type="transfer",
            direction="debit",
            counterparty_account="NABIL-1001",
            counterparty_name="Himalayan Utilities",
            country="NP",
            city="Kathmandu",
            device_id="DEVICE-MAYA-01",
            ip_address="103.1.1.10",
            channel="mobile",
            status="completed",
            occurred_at=datetime(
                2026,
                8,
                5,
                10,
                15,
                tzinfo=timezone.utc,
            ),
        )

        normal_transaction_2 = Transaction(
            transaction_reference="TXN-002",
            account=account,
            amount=Decimal("6200.00"),
            currency="NPR",
            transaction_type="transfer",
            direction="debit",
            counterparty_account="NABIL-2002",
            counterparty_name="Kathmandu Internet Services",
            country="NP",
            city="Kathmandu",
            device_id="DEVICE-MAYA-01",
            ip_address="103.1.1.10",
            channel="mobile",
            status="completed",
            occurred_at=datetime(
                2026,
                8,
                12,
                11,
                30,
                tzinfo=timezone.utc,
            ),
        )

        normal_transaction_3 = Transaction(
            transaction_reference="TXN-003",
            account=account,
            amount=Decimal("3800.00"),
            currency="NPR",
            transaction_type="transfer",
            direction="debit",
            counterparty_account="NABIL-1001",
            counterparty_name="Himalayan Utilities",
            country="NP",
            city="Kathmandu",
            device_id="DEVICE-MAYA-01",
            ip_address="103.1.1.10",
            channel="mobile",
            status="completed",
            occurred_at=datetime(
                2026,
                8,
                20,
                9,
                45,
                tzinfo=timezone.utc,
            ),
        )

        alerted_transaction = Transaction(
            transaction_reference="TXN-004",
            account=account,
            amount=Decimal("450000.00"),
            currency="NPR",
            transaction_type="transfer",
            direction="debit",
            counterparty_account="INTL-9001",
            counterparty_name="Global Trade Solutions",
            country="SG",
            city="Singapore",
            device_id="DEVICE-UNKNOWN-99",
            ip_address="203.0.113.50",
            channel="web",
            status="completed",
            occurred_at=datetime(
                2026,
                9,
                1,
                2,
                20,
                tzinfo=timezone.utc,
            ),
        )

        fraud_alert = FraudAlert(
            alert_reference="ALERT-001",
            transaction=alerted_transaction,
            alert_type="high_amount",
            severity="high",
            status="open",
            reason=(
                "Transaction amount is significantly higher than the customer's "
                "recent transaction history."
            ),
            triggered_at=datetime(
                2026,
                9,
                1,
                2,
                21,
                tzinfo=timezone.utc,
            ),
        )

        db.add_all(
            [
                customer,
                account,
                normal_transaction_1,
                normal_transaction_2,
                normal_transaction_3,
                alerted_transaction,
                fraud_alert,
            ]
        )
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_financial_data()