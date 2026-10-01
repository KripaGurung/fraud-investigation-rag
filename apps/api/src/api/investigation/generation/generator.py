from typing import Protocol


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