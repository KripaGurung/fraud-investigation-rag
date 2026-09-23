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
from api.investigation.evaluation.semantic_evaluator import (
    FindingSemanticEvaluation,
    evaluate_case_semantic_groundedness,
)
from api.investigation.evaluation.semantic_groundedness import (
    SemanticGroundednessEvaluator,
)
from api.investigation.generation.schemas import InvestigationCase


@dataclass(frozen=True)
class InvestigationEvaluationResult:
    """Combined evaluation results for a generated investigation case."""

    completeness: ReportCompletenessResult
    groundedness: GroundednessResult
    semantic_groundedness: list[FindingSemanticEvaluation] | None = None

def evaluate_investigation(
    case: InvestigationCase,
    context: InvestigationContext,
    semantic_evaluator: SemanticGroundednessEvaluator | None = None,
) -> InvestigationEvaluationResult:
    """Evaluate a generated investigation across supported dimensions."""
    semantic_groundedness = (
        evaluate_case_semantic_groundedness(
            case,
            context,
            semantic_evaluator,
        )
        if semantic_evaluator is not None
        else None
    )

    return InvestigationEvaluationResult(
        completeness=evaluate_report_completeness(case),
        groundedness=evaluate_groundedness(
            case,
            context,
        ),
        semantic_groundedness=semantic_groundedness,
    )