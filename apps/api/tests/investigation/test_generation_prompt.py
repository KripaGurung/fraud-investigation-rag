from api.investigation.context import InvestigationContext
from api.investigation.generation.prompt import (
    SYSTEM_PROMPT,
    build_investigation_prompt,
)
from api.investigation.schemas import (
    AnalyzedEvidence,
    EvidenceClassification,
)
from api.schemas.evidence import EvidenceItem


def make_evidence(
    source_id: str,
    source_type: str,
    content: str,
    score: float = 0.9,
) -> EvidenceItem:
    return EvidenceItem(
        source_id=source_id,
        source_type=source_type,
        content=content,
        score=score,
        metadata={
            "title": f"Title for {source_id}",
            "source": "test-source",
            "chunk_id": 1,
            "chunk_index": 0,
        },
    )


def test_system_prompt_requires_evidence_grounding() -> None:
    assert "ONLY the evidence provided" in SYSTEM_PROMPT
    assert "Do not invent" in SYSTEM_PROMPT
    assert "supporting evidence" in SYSTEM_PROMPT
    assert "contradicting evidence" in SYSTEM_PROMPT
    assert "missing evidence" in SYSTEM_PROMPT


def test_build_investigation_prompt_separates_evidence_categories() -> None:
    supporting = AnalyzedEvidence(
        evidence=make_evidence(
            source_id="CASE-001",
            source_type="historical_fraud_case",
            content="A similar transaction involved a new beneficiary.",
        ),
        classification=EvidenceClassification.SUPPORTING,
        explanation="Supporting evidence.",
    )

    contradicting = AnalyzedEvidence(
        evidence=make_evidence(
            source_id="CASE-002",
            source_type="historical_fraud_case",
            content="The customer's previous transaction was legitimate.",
        ),
        classification=EvidenceClassification.CONTRADICTING,
        explanation="Contradicting evidence.",
    )

    neutral = AnalyzedEvidence(
        evidence=make_evidence(
            source_id="POLICY-AML-001",
            source_type="aml_policy",
            content="Transactions outside established patterns may require review.",
        ),
        classification=EvidenceClassification.NEUTRAL,
        explanation="Neutral evidence.",
    )

    context = InvestigationContext(
        analyzed_evidence=[
            supporting,
            contradicting,
            neutral,
        ],
        missing_evidence=["customer_identity_verification"],
    )

    prompt = build_investigation_prompt(context)

    assert "SUPPORTING EVIDENCE" in prompt
    assert "CONTRADICTING EVIDENCE" in prompt
    assert "NEUTRAL EVIDENCE" in prompt
    assert "MISSING EVIDENCE" in prompt

    assert "CASE-001" in prompt
    assert "CASE-002" in prompt
    assert "POLICY-AML-001" in prompt
    assert "customer_identity_verification" in prompt


def test_build_investigation_prompt_preserves_evidence_content() -> None:
    evidence = AnalyzedEvidence(
        evidence=make_evidence(
            source_id="TXN-004",
            source_type="transaction",
            content=(
                "Transaction amount was 450000.00 NPR "
                "from Singapore, SG using DEVICE-UNKNOWN-99."
            ),
        ),
        classification=EvidenceClassification.SUPPORTING,
        explanation="Supporting evidence.",
    )

    context = InvestigationContext(
        analyzed_evidence=[evidence],
        missing_evidence=[],
    )

    prompt = build_investigation_prompt(context)

    assert "TXN-004" in prompt
    assert "450000.00 NPR" in prompt
    assert "Singapore, SG" in prompt
    assert "DEVICE-UNKNOWN-99" in prompt


def test_build_investigation_prompt_handles_empty_categories() -> None:
    context = InvestigationContext(
        analyzed_evidence=[],
        missing_evidence=[],
    )

    prompt = build_investigation_prompt(context)

    assert "SUPPORTING EVIDENCE" in prompt
    assert "CONTRADICTING EVIDENCE" in prompt
    assert "NEUTRAL EVIDENCE" in prompt
    assert "MISSING EVIDENCE" in prompt

    assert "None." in prompt