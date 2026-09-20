from api.schemas.evidence import EvidenceBundle


def detect_missing_evidence(bundle: EvidenceBundle) -> list[str]:
    """Detect evidence categories that are absent from the bundle."""
    missing = []

    if not bundle.transaction_evidence:
        missing.append("transaction_evidence")

    if not bundle.historical_case_evidence:
        missing.append("historical_case_evidence")

    if not bundle.policy_evidence:
        missing.append("policy_evidence")

    return missing