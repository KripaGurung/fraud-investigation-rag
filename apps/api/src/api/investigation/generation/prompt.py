from api.investigation.context import InvestigationContext


def build_investigation_prompt(
    alert_id: str,
    context: InvestigationContext,
) -> str:
    """Build a grounded prompt from structured investigation context."""
    evidence_sections = []

    for analyzed in context.analyzed_evidence:
        evidence = analyzed.evidence
        evidence_sections.append(
            "\n".join(
                [
                    f"Evidence ID: {evidence.source_id}",
                    f"Source type: {evidence.source_type}",
                    f"Classification: {analyzed.classification.value}",
                    f"Content: {evidence.content}",
                    f"Analysis: {analyzed.explanation}",
                ]
            )
        )

    evidence_text = "\n\n".join(evidence_sections)
    missing_text = ", ".join(context.missing_evidence) or "None"

    return f"""Generate a structured investigation case for alert {alert_id}.

Use only the evidence provided below.
Do not invent evidence, facts, or evidence IDs.
Do not make a final fraud determination.
Preserve uncertainty and contradictory evidence.
Every generated finding must reference only Evidence IDs listed below.

Evidence:
{evidence_text}

Missing evidence:
{missing_text}
"""