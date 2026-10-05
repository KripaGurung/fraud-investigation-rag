from types import SimpleNamespace

from api.investigation.context import build_investigation_context
from api.investigation.generation.generator import InvestigationGenerator
from api.investigation.generation.openai_generator import (
    OpenAIInvestigationGenerator,
)
from api.investigation.generation.schemas import (
    InvestigationCase,
    InvestigationFinding,
)
from tests.fixtures.evidence_bundles import clearly_suspicious_bundle


class FakeResponses:
    def __init__(self, parsed_case: InvestigationCase) -> None:
        self.parsed_case = parsed_case
        self.received_model: str | None = None
        self.received_input: str | None = None
        self.received_format: type[InvestigationCase] | None = None

    def parse(
        self,
        *,
        model: str,
        input: str,
        text_format: type[InvestigationCase],
    ) -> SimpleNamespace:
        self.received_model = model
        self.received_input = input
        self.received_format = text_format

        return SimpleNamespace(
            output_parsed=self.parsed_case,
        )


class FakeOpenAIClient:
    def __init__(self, parsed_case: InvestigationCase) -> None:
        self.responses = FakeResponses(parsed_case)


def test_openai_generator_satisfies_protocol() -> None:
    fake_case = InvestigationCase(
        alert_id="alert-suspicious-001",
        executive_summary="Test summary.",
        risk_narrative="Test risk narrative.",
    )
    client = FakeOpenAIClient(fake_case)

    generator = OpenAIInvestigationGenerator(client=client)

    assert isinstance(generator, InvestigationGenerator)


def test_openai_generator_returns_structured_case() -> None:
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    fake_case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="The alert requires further investigation.",
        risk_narrative="The activity is inconsistent with prior behavior.",
        supporting_findings=[
            InvestigationFinding(
                statement="The transaction is unusually large.",
                evidence_ids=["txn-001"],
            )
        ],
        missing_evidence=[],
        recommended_follow_up=["Review the customer relationship."],
    )

    client = FakeOpenAIClient(fake_case)
    generator = OpenAIInvestigationGenerator(client=client)

    result = generator.generate(bundle.alert_id, context)

    assert result == fake_case
    assert result.alert_id == bundle.alert_id
    assert result.supporting_findings[0].evidence_ids == ["txn-001"]


def test_openai_generator_sends_grounded_prompt_to_client() -> None:
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    fake_case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test risk narrative.",
    )

    client = FakeOpenAIClient(fake_case)
    generator = OpenAIInvestigationGenerator(client=client)

    generator.generate(bundle.alert_id, context)

    assert client.responses.received_input is not None
    assert bundle.alert_id in client.responses.received_input
    assert "txn-001" in client.responses.received_input
    assert "case-001" in client.responses.received_input
    assert "policy-001" in client.responses.received_input


def test_openai_generator_uses_investigation_case_as_response_format() -> None:
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    fake_case = InvestigationCase(
        alert_id=bundle.alert_id,
        executive_summary="Test summary.",
        risk_narrative="Test risk narrative.",
    )

    client = FakeOpenAIClient(fake_case)
    generator = OpenAIInvestigationGenerator(client=client)

    generator.generate(bundle.alert_id, context)

    assert client.responses.received_format is InvestigationCase

def test_openai_generator_requires_api_key(monkeypatch) -> None:
    monkeypatch.setattr(
        "api.investigation.generation.openai_generator.settings.openai_api_key",
        None,
    )

    try:
        OpenAIInvestigationGenerator()
    except ValueError as exc:
        assert "OPENAI_API_KEY" in str(exc)
    else:
        raise AssertionError("Expected ValueError when API key is missing")  

def test_openai_generator_rejects_missing_structured_output() -> None:
    bundle = clearly_suspicious_bundle()
    context = build_investigation_context(bundle)

    class EmptyResponses:
        def parse(
            self,
            *,
            model: str,
            input: str,
            text_format: type[InvestigationCase],
        ) -> SimpleNamespace:
            return SimpleNamespace(output_parsed=None)

    class EmptyOpenAIClient:
        def __init__(self) -> None:
            self.responses = EmptyResponses()

    generator = OpenAIInvestigationGenerator(
        client=EmptyOpenAIClient(),
    )

    try:
        generator.generate(bundle.alert_id, context)
    except ValueError as exc:
        assert "no structured investigation case" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError when structured output is missing"
        )      

    