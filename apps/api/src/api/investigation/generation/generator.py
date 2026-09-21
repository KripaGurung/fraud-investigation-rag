from typing import Protocol, runtime_checkable

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