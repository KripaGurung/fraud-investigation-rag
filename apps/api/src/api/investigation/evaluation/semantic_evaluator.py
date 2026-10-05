from dataclasses import dataclass

from api.investigation.context import InvestigationContext
from api.investigation.evaluation.semantic_groundedness import (
    SemanticGroundednessEvaluator,
    SemanticGroundednessResult,
)
from api.investigation.generation.schemas import InvestigationCase


@dataclass(frozen=True)
class FindingSemanticEvaluation:
    """Semantic grounding result for one generated investigation finding."""

    statement: str
    evidence_ids: list[str]
    result: SemanticGroundednessResult


@dataclass(frozen=True)
class CaseSemanticGroundednessResult:
    """Aggregate semantic grounding result for an investigation case."""

    score: float
    total_findings: int
    supported_findings: int
    unsupported_findings: list[FindingSemanticEvaluation]
    finding_evaluations: list[FindingSemanticEvaluation]


def _build_evidence_content_map(
    context: InvestigationContext,
) -> dict[str, str]:
    """Map available evidence IDs to their content."""
    return {
        analyzed.evidence.source_id: analyzed.evidence.content
        for analyzed in context.analyzed_evidence
    }


def evaluate_finding_semantic_groundedness(
    statement: str,
    evidence_ids: list[str],
    evidence_content_map: dict[str, str],
    evaluator: SemanticGroundednessEvaluator,
) -> FindingSemanticEvaluation:
    """Evaluate whether a finding is supported by its cited evidence."""
    evidence_contents = [
        evidence_content_map[evidence_id]
        for evidence_id in evidence_ids
        if evidence_id in evidence_content_map
    ]

    result = evaluator.evaluate(
        statement=statement,
        evidence_contents=evidence_contents,
    )

    return FindingSemanticEvaluation(
        statement=statement,
        evidence_ids=evidence_ids,
        result=result,
    )


def evaluate_case_semantic_groundedness(
    case: InvestigationCase,
    context: InvestigationContext,
    evaluator: SemanticGroundednessEvaluator,
) -> CaseSemanticGroundednessResult:
    """Evaluate semantic grounding for all findings in an investigation case."""
    evidence_content_map = _build_evidence_content_map(context)

    findings = (
        case.supporting_findings
        + case.contradicting_findings
    )

    finding_evaluations = [
        evaluate_finding_semantic_groundedness(
            statement=finding.statement,
            evidence_ids=finding.evidence_ids,
            evidence_content_map=evidence_content_map,
            evaluator=evaluator,
        )
        for finding in findings
    ]

    unsupported_findings = [
        evaluation
        for evaluation in finding_evaluations
        if not evaluation.result.is_supported
    ]

    total_findings = len(finding_evaluations)
    supported_findings = total_findings - len(unsupported_findings)

    score = (
        supported_findings / total_findings
        if total_findings
        else 1.0
    )

    return CaseSemanticGroundednessResult(
        score=score,
        total_findings=total_findings,
        supported_findings=supported_findings,
        unsupported_findings=unsupported_findings,
        finding_evaluations=finding_evaluations,
    )