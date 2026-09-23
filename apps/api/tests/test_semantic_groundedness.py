from api.investigation.evaluation.semantic_groundedness import (
    SemanticGroundednessEvaluator,
    SemanticGroundednessResult,
)


class FakeSemanticGroundednessEvaluator:
    def evaluate(
        self,
        statement: str,
        evidence_contents: list[str],
    ) -> SemanticGroundednessResult:
        return SemanticGroundednessResult(
            is_supported=True,
            explanation="The finding is supported by the cited evidence.",
        )


def test_semantic_groundedness_evaluator_protocol():
    evaluator = FakeSemanticGroundednessEvaluator()

    assert isinstance(
        evaluator,
        SemanticGroundednessEvaluator,
    )