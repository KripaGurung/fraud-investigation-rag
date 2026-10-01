from api.investigation.generation.generator import (
    DeterministicReportGenerator,
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