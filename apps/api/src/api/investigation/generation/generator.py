from typing import Protocol, runtime_checkable

from google import genai

from api.investigation.context import InvestigationContext
from api.investigation.generation.schemas import InvestigationCase


@runtime_checkable
class InvestigationGenerator(Protocol):
    """Contract for investigation case generation implementations."""

    def generate(
        self,
        alert_id: str,
        context: InvestigationContext,
    ) -> InvestigationCase:
        """Generate a structured investigation case from investigation context."""
        ...


class InvestigationReportGenerator(Protocol):
    """Contract for generating investigator-facing reports."""

    def generate(
        self,
        system_prompt: str,
        investigation_prompt: str,
    ) -> str:
        """Generate a report from grounded investigation prompts."""
        ...


class DeterministicReportGenerator:
    """Deterministic generator used for local development and testing."""

    def generate(
        self,
        system_prompt: str,
        investigation_prompt: str,
    ) -> str:
        return (
            "Investigation report generated from the provided evidence. "
            "A production LLM generator can replace this implementation "
            "without changing the investigation pipeline."
        )


class GeminiReportGenerator:
    """Gemini implementation for generating investigation reports."""

    def __init__(
        self,
        api_key: str,
        model: str,
    ) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(
        self,
        system_prompt: str,
        investigation_prompt: str,
    ) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=investigation_prompt,
            config={
                "system_instruction": system_prompt,
            },
        )

        if response.text is None:
            raise ValueError("Gemini returned an empty investigation report.")

        return response.text