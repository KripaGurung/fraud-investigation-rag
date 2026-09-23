from dataclasses import dataclass

from api.investigation.context import InvestigationContext
from api.investigation.evaluation.completeness import (
    ReportCompletenessResult,
    evaluate_report_completeness,
)
from api.investigation.evaluation.groundedness import (
    GroundednessResult,
    evaluate_groundedness,
)
from api.investigation.generation.schemas import InvestigationCase


@dataclass(frozen=True)
class InvestigationEvaluationResult:
    """Combined evaluation results for a generated investigation case."""

    completeness: ReportCompletenessResult
    groundedness: GroundednessResult

def evaluate_investigation(
    case: InvestigationCase,
    context: InvestigationContext,
) -> InvestigationEvaluationResult:
    """Evaluate a generated investigation across supported dimensions."""
    return InvestigationEvaluationResult(
        completeness=evaluate_report_completeness(case),
        groundedness=evaluate_groundedness(
            case,
            context,
        ),
    )    