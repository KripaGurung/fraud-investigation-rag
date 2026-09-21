from sqlalchemy.orm import Session

from api.rag.retrieval.hybrid import hybrid_search
from api.schemas.evidence import EvidenceBundle, EvidenceItem
from api.services.investigation import InvestigationContext
from api.services.rag_evidence import retrieval_result_to_evidence


def build_evidence_bundle(
    db: Session,
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

    retrieval_query = (
        f"Transaction type: {transaction.transaction_type}. "
        f"Amount: {transaction.amount} {transaction.currency}. "
        f"Direction: {transaction.direction}. "
        f"Channel: {transaction.channel}. "
        f"Location: {transaction.city}, {transaction.country}. "
        f"Counterparty: {transaction.counterparty_name}. "
        f"Device: {transaction.device_id}. "
        f"Alert type: {alert.alert_type}. "
        f"Alert reason: {alert.reason}."
    )

    historical_case_results = hybrid_search(
        db=db,
        query=retrieval_query,
        limit=5,
        document_type="historical_fraud_case",
    )

    policy_results = hybrid_search(
        db=db,
        query=retrieval_query,
        limit=5,
        document_type="aml_policy",
    )

    historical_case_evidence = [
        retrieval_result_to_evidence(result)
        for result in historical_case_results
    ]

    policy_evidence = [
        retrieval_result_to_evidence(result)
        for result in policy_results
    ]

    return EvidenceBundle(
        alert_id=alert.alert_reference,
        transaction_evidence=transaction_evidence,
        historical_case_evidence=historical_case_evidence,
        policy_evidence=policy_evidence,
    )