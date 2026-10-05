from api.investigation.context import InvestigationContext
from api.investigation.generation.generator import InvestigationGenerator
from api.investigation.generation.schemas import InvestigationCase


class FakeInvestigationGenerator:
    def generate(
        self,
        alert_id: str,
        context: InvestigationContext,
    ) -> InvestigationCase:
        return InvestigationCase(
            alert_id=alert_id,
            executive_summary="Test investigation summary.",
            risk_narrative="Test risk narrative.",
        )


def test_generator_implementation_satisfies_protocol() -> None:
    generator = FakeInvestigationGenerator()

    assert isinstance(generator, InvestigationGenerator)