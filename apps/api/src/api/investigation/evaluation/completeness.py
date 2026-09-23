from dataclasses import dataclass, field

from api.investigation.generation.schemas import InvestigationCase


@dataclass(frozen=True)
class ReportCompletenessResult:
    """Result of evaluating required investigation report sections."""

    is_complete: bool
    missing_sections: list[str] = field(default_factory=list)

REQUIRED_REPORT_SECTIONS = (
    "executive_summary",
    "risk_narrative",
    "supporting_findings",
)  

def _is_section_empty(value: object) -> bool:
    """Return whether a required report section has no meaningful content."""
    if isinstance(value, str):
        return not value.strip()

    return not value

def evaluate_report_completeness(
    case: InvestigationCase,
) -> ReportCompletenessResult:
    """Evaluate whether required investigation report sections are populated."""
    missing_sections = [
        section
        for section in REQUIRED_REPORT_SECTIONS
        if _is_section_empty(getattr(case, section))
    ]

    return ReportCompletenessResult(
        is_complete=not missing_sections,
        missing_sections=missing_sections,
    )