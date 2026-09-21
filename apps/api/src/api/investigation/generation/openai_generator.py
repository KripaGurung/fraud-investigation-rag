from openai import OpenAI

from api.core.config import settings
from api.investigation.context import InvestigationContext
from api.investigation.generation.generator import InvestigationGenerator
from api.investigation.generation.prompt import build_investigation_prompt
from api.investigation.generation.schemas import InvestigationCase


class OpenAIInvestigationGenerator(InvestigationGenerator):
    """Generate investigator-ready cases using OpenAI structured outputs."""

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
                "OpenAIInvestigationGenerator."
            )

        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate(
        self,
        alert_id: str,
        context: InvestigationContext,
    ) -> InvestigationCase:
        prompt = build_investigation_prompt(
            alert_id,
            context,
        )

        response = self.client.responses.parse(
            model=settings.openai_model,
            input=prompt,
            text_format=InvestigationCase,
        )

        if response.output_parsed is None:
            raise ValueError(
                "OpenAI returned no structured investigation case."
            )

        return response.output_parsed