from api.investigation.context import InvestigationContext
from api.investigation.schemas import EvidenceClassification


SYSTEM_PROMPT = """You are a financial fraud investigation assistant.

Your task is to prepare a concise, evidence-grounded investigation report
for a human investigator.

Use ONLY the evidence provided in the investigation context.

Do not invent transactions, customers, policies, facts, explanations,
or conclusions that are not supported by the provided evidence.

Clearly distinguish:
- supporting evidence
- contradicting evidence
- missing evidence

Every factual statement in the report must be traceable to the provided
evidence.

If evidence is insufficient, explicitly state that additional investigation
or evidence is required.

Do not make a definitive fraud determination unless the provided evidence
explicitly supports such a determination.
"""


def build_investigation_prompt(
    context: InvestigationContext,
) -> str:
    supporting = []
    contradicting = []
    neutral = []

    for item in context.analyzed_evidence:
        evidence = item.evidence

        formatted = (
            f"Source ID: {evidence.source_id}\n"
            f"Source type: {evidence.source_type}\n"
            f"Score: {evidence.score:.4f}\n"
            f"Content: {evidence.content}\n"
        )

        if item.classification == EvidenceClassification.SUPPORTING:
            supporting.append(formatted)

        elif item.classification == EvidenceClassification.CONTRADICTING:
            contradicting.append(formatted)

        else:
            neutral.append(formatted)

    return f"""Prepare an investigation report using the following evidence.

SUPPORTING EVIDENCE
===================
{_format_evidence(supporting)}

CONTRADICTING EVIDENCE
======================
{_format_evidence(contradicting)}

NEUTRAL EVIDENCE
================
{_format_evidence(neutral)}

MISSING EVIDENCE
===============
{_format_missing_evidence(context.missing_evidence)}

REPORT REQUIREMENTS
===================
1. Summarize the alert and the evidence relevant to it.
2. Explain the main indicators that support further investigation.
3. Identify any evidence that contradicts or weakens the indicators.
4. Explicitly identify missing evidence.
5. Do not introduce facts that are not present in the evidence.
6. Keep the report concise and suitable for a fraud investigator.
"""


def _format_evidence(evidence: list[str]) -> str:
    if not evidence:
        return "None."

    return "\n".join(
        f"[{index}] {item}"
        for index, item in enumerate(evidence, start=1)
    )


def _format_missing_evidence(
    missing_evidence: list[str],
) -> str:
    if not missing_evidence:
        return "None."

    return "\n".join(
        f"- {item}"
        for item in missing_evidence
    )