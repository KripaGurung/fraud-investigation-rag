from openai import OpenAI

from pydantic import BaseModel

from api.core.config import settings
from api.investigation.evaluation.semantic_groundedness import (
    SemanticGroundednessEvaluator,
    SemanticGroundednessResult,
)

class SemanticGroundednessJudgment(BaseModel):
    """Structured semantic-support judgment returned by the LLM."""

    is_supported: bool
    explanation: str

def _build_semantic_groundedness_prompt(
    statement: str,
    evidence_contents: list[str],
) -> str:
    """Build a prompt for evaluating whether evidence supports a finding."""
    evidence_text = "\n".join(
        f"- {content}"
        for content in evidence_contents
    )

    return f"""
Evaluate whether the generated investigation finding is supported by the
provided evidence.

Generated finding:
{statement}

Cited evidence:
{evidence_text}

Rules:
- Use only the provided evidence.
- Do not use outside knowledge.
- Mark the finding as supported only when the evidence supports the claim.
- If the evidence contradicts the finding, mark it as unsupported.
- If the evidence is insufficient to establish the finding, mark it as unsupported.
- Explain the judgment briefly.
""".strip()

class OpenAISemanticGroundednessEvaluator(SemanticGroundednessEvaluator):
    """Evaluate semantic evidence support using OpenAI."""

    def __init__(
        self,
        client: OpenAI | None = None,
    ) -> None:
        if client is not None:
            self.client = client
            return

        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY must be configured to use "
                "OpenAISemanticGroundednessEvaluator."
            )

        self.client = OpenAI(api_key=settings.openai_api_key)

    def evaluate(
    self,
    statement: str,
    evidence_contents: list[str],
    ) -> SemanticGroundednessResult:
        """Evaluate whether cited evidence semantically supports a finding."""
        prompt = _build_semantic_groundedness_prompt(
            statement,
            evidence_contents,
        )

        response = self.client.responses.parse(
           model=settings.openai_model,
           input=prompt,
           text_format=SemanticGroundednessJudgment,
        )

        if response.output_parsed is None:
            raise ValueError(
                "OpenAI returned no structured semantic groundedness judgment."
            )

        judgment = response.output_parsed

        return SemanticGroundednessResult(
            is_supported=judgment.is_supported,
            explanation=judgment.explanation,
        )    