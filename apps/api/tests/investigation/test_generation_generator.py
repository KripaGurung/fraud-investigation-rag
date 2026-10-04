from unittest.mock import Mock

from api.investigation.generation.generator import (
    DeterministicReportGenerator,
    GeminiReportGenerator,
    InvestigationReportGenerator,
)


def test_deterministic_report_generator_satisfies_contract() -> None:
    generator: InvestigationReportGenerator = DeterministicReportGenerator()

    report = generator.generate(
        system_prompt="System instructions.",
        investigation_prompt="Investigation evidence.",
    )

    assert isinstance(report, str)
    assert report.strip()


def test_deterministic_report_generator_returns_stable_output() -> None:
    generator = DeterministicReportGenerator()

    first_report = generator.generate(
        system_prompt="System instructions.",
        investigation_prompt="Investigation evidence.",
    )

    second_report = generator.generate(
        system_prompt="System instructions.",
        investigation_prompt="Investigation evidence.",
    )

    assert first_report == second_report


def test_deterministic_report_generator_mentions_evidence() -> None:
    generator = DeterministicReportGenerator()

    report = generator.generate(
        system_prompt="System instructions.",
        investigation_prompt="Investigation evidence.",
    )

    assert "provided evidence" in report.lower()


def test_gemini_report_generator_satisfies_contract() -> None:
    generator: InvestigationReportGenerator = GeminiReportGenerator(
        api_key="test-api-key",
        model="gemini-2.5-flash",
    )

    assert isinstance(generator, GeminiReportGenerator)


def test_gemini_report_generator_returns_generated_report() -> None:
    generator = GeminiReportGenerator(
        api_key="test-api-key",
        model="gemini-2.5-flash",
    )

    mock_response = Mock()
    mock_response.text = "Grounded investigation report."

    generator.client.models.generate_content = Mock(
        return_value=mock_response,
    )

    report = generator.generate(
        system_prompt="Use only provided evidence.",
        investigation_prompt="Supporting evidence: transaction history.",
    )

    assert report == "Grounded investigation report."

    generator.client.models.generate_content.assert_called_once_with(
        model="gemini-2.5-flash",
        contents="Supporting evidence: transaction history.",
        config={
            "system_instruction": "Use only provided evidence.",
        },
    )