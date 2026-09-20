from api.schemas.evidence import EvidenceBundle, EvidenceItem


def clearly_suspicious_bundle() -> EvidenceBundle:
    return EvidenceBundle(
        alert_id="alert-suspicious-001",
        transaction_evidence=[
            EvidenceItem(
                source_id="txn-001",
                source_type="transaction",
                content="Transaction amount is significantly above the customer's usual range.",
                score=0.95,
                metadata={"transaction_id": "txn-001"},
            )
        ],
        historical_case_evidence=[
            EvidenceItem(
                source_id="case-001",
                source_type="historical_case",
                content="A previous fraud case involved a similar unusually large transaction pattern.",
                score=0.88,
                metadata={"case_id": "case-001"},
            )
        ],
        policy_evidence=[
            EvidenceItem(
                source_id="policy-001",
                source_type="policy",
                content="Transactions significantly outside established customer behavior require investigation.",
                score=0.91,
                metadata={"policy_id": "policy-001"},
            )
        ],
    )


def contradictory_context_bundle() -> EvidenceBundle:
    return EvidenceBundle(
        alert_id="alert-contradictory-001",
        transaction_evidence=[
            EvidenceItem(
                source_id="txn-002",
                source_type="transaction",
                content="Transaction amount is significantly above the customer's usual range.",
                score=0.94,
                metadata={"transaction_id": "txn-002"},
            )
        ],
        historical_case_evidence=[
            EvidenceItem(
                source_id="case-002",
                source_type="historical_case",
                content="Similar large transactions were previously reviewed and confirmed as legitimate business payments.",
                score=0.87,
                metadata={"case_id": "case-002"},
            )
        ],
        policy_evidence=[
            EvidenceItem(
                source_id="policy-002",
                source_type="policy",
                content="Unusual transaction amounts require review alongside available customer context.",
                score=0.90,
                metadata={"policy_id": "policy-002"},
            )
        ],
    )


def mixed_evidence_bundle() -> EvidenceBundle:
    return EvidenceBundle(
        alert_id="alert-mixed-001",
        transaction_evidence=[
            EvidenceItem(
                source_id="txn-003",
                source_type="transaction",
                content="A large transaction was sent to a beneficiary not previously used by the customer.",
                score=0.93,
                metadata={"transaction_id": "txn-003"},
            )
        ],
        historical_case_evidence=[
            EvidenceItem(
                source_id="case-003",
                source_type="historical_case",
                content="The customer has previously made legitimate high-value payments to new beneficiaries.",
                score=0.84,
                metadata={"case_id": "case-003"},
            )
        ],
        policy_evidence=[
            EvidenceItem(
                source_id="policy-003",
                source_type="policy",
                content="High-value payments to new beneficiaries require additional review.",
                score=0.89,
                metadata={"policy_id": "policy-003"},
            )
        ],
    )


def insufficient_evidence_bundle() -> EvidenceBundle:
    return EvidenceBundle(
        alert_id="alert-insufficient-001",
        transaction_evidence=[
            EvidenceItem(
                source_id="txn-004",
                source_type="transaction",
                content="A transaction triggered an alert for an unusually high amount.",
                score=0.90,
                metadata={"transaction_id": "txn-004"},
            )
        ],
        historical_case_evidence=[],
        policy_evidence=[],
    )


def policy_without_history_bundle() -> EvidenceBundle:
    return EvidenceBundle(
        alert_id="alert-policy-no-history-001",
        transaction_evidence=[
            EvidenceItem(
                source_id="txn-005",
                source_type="transaction",
                content="A high-value transaction was sent to a newly observed beneficiary.",
                score=0.92,
                metadata={"transaction_id": "txn-005"},
            )
        ],
        historical_case_evidence=[],
        policy_evidence=[
            EvidenceItem(
                source_id="policy-005",
                source_type="policy",
                content="High-value transactions to new beneficiaries require review against available customer history.",
                score=0.93,
                metadata={"policy_id": "policy-005"},
            )
        ],
    )

