from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class FraudAlertSummary(BaseModel):
    """Investigator-facing summary of a fraud alert."""

    model_config = ConfigDict(from_attributes=True)

    alert_reference: str
    alert_type: str
    severity: str
    status: str
    reason: str
    triggered_at: datetime

class TransactionDetail(BaseModel):
    """Investigator-facing transaction details."""

    model_config = ConfigDict(from_attributes=True)

    transaction_reference: str
    amount: Decimal
    currency: str
    transaction_type: str
    direction: str
    counterparty_account: str | None
    counterparty_name: str | None
    country: str | None
    city: str | None
    device_id: str | None
    ip_address: str | None
    channel: str
    status: str
    occurred_at: datetime    

class AccountDetail(BaseModel):
    """Investigator-facing account details."""

    model_config = ConfigDict(from_attributes=True)

    account_number: str
    account_type: str
    currency: str
    status: str
    current_balance: Decimal
    opened_at: datetime    

class CustomerDetail(BaseModel):
    """Investigator-facing customer details."""

    model_config = ConfigDict(from_attributes=True)

    customer_number: str
    full_name: str
    country: str
    risk_level: str
    kyc_status: str    

class FraudAlertDetail(BaseModel):
    """Complete investigator-facing fraud alert details."""

    alert_reference: str
    alert_type: str
    severity: str
    status: str
    reason: str
    triggered_at: datetime
    transaction: TransactionDetail
    account: AccountDetail
    customer: CustomerDetail    