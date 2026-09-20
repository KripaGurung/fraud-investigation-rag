from api.schemas.evidence import EvidenceBundle, EvidenceItem
from api.services.investigation import InvestigationContext


def build_evidence_bundle(
    context: InvestigationContext,
) -> EvidenceBundle:
    transaction = context.transaction
    alert = context.alert

    transaction_evidence = [
        EvidenceItem(
            source_id=alert.alert_reference,
            source_type="fraud_alert",
            content=(
                f"Fraud alert {alert.alert_reference} was triggered for "
                f"transaction {transaction.transaction_reference}. "
                f"Alert type: {alert.alert_type}. "
                f"Severity: {alert.severity}. "
                f"Reason: {alert.reason}"
            ),
            score=1.0,
            metadata={
                "alert_reference": alert.alert_reference,
                "alert_type": alert.alert_type,
                "severity": alert.severity,
                "status": alert.status,
            },
        ),
        EvidenceItem(
            source_id=transaction.transaction_reference,
            source_type="transaction",
            content=(
                f"Transaction {transaction.transaction_reference}: "
                f"{transaction.amount} {transaction.currency} "
                f"{transaction.direction} {transaction.transaction_type} "
                f"via {transaction.channel}. "
                f"Location: {transaction.city}, {transaction.country}. "
                f"Counterparty: {transaction.counterparty_name}. "
                f"Device: {transaction.device_id}."
            ),
            score=1.0,
            metadata={
                "transaction_reference": transaction.transaction_reference,
                "amount": str(transaction.amount),
                "currency": transaction.currency,
                "direction": transaction.direction,
                "transaction_type": transaction.transaction_type,
                "channel": transaction.channel,
                "country": transaction.country,
                "city": transaction.city,
                "device_id": transaction.device_id,
            },
        ),
    ]

    historical_case_evidence = [
        EvidenceItem(
            source_id=historical_transaction.transaction_reference,
            source_type="transaction_history",
            content=(
                f"Historical transaction "
                f"{historical_transaction.transaction_reference}: "
                f"{historical_transaction.amount} "
                f"{historical_transaction.currency} "
                f"{historical_transaction.direction} "
                f"{historical_transaction.transaction_type} "
                f"via {historical_transaction.channel}. "
                f"Location: {historical_transaction.city}, "
                f"{historical_transaction.country}. "
                f"Counterparty: "
                f"{historical_transaction.counterparty_name}. "
                f"Device: {historical_transaction.device_id}."
            ),
            score=1.0,
            metadata={
                "transaction_reference": (
                    historical_transaction.transaction_reference
                ),
                "amount": str(historical_transaction.amount),
                "currency": historical_transaction.currency,
                "direction": historical_transaction.direction,
                "transaction_type": historical_transaction.transaction_type,
                "channel": historical_transaction.channel,
                "country": historical_transaction.country,
                "city": historical_transaction.city,
                "device_id": historical_transaction.device_id,
                "occurred_at": (
                    historical_transaction.occurred_at.isoformat()
                ),
            },
        )
        for historical_transaction in context.historical_transactions
    ]

    return EvidenceBundle(
        alert_id=alert.alert_reference,
        transaction_evidence=transaction_evidence,
        historical_case_evidence=historical_case_evidence,
        policy_evidence=[],
    )