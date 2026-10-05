import pytest

from api.investigation.evaluation.openai_semantic_groundedness import (
    OpenAISemanticGroundednessEvaluator,
    SemanticGroundednessJudgment,
)


class FakeResponse:
    def __init__(
        self,
        output_parsed: SemanticGroundednessJudgment | None,
    ) -> None:
        self.output_parsed = output_parsed


class FakeResponses:
    def __init__(
        self,
        output_parsed: SemanticGroundednessJudgment | None,
    ) -> None:
        self.output_parsed = output_parsed

    def parse(self, **kwargs):
        return FakeResponse(self.output_parsed)


class FakeOpenAI:
    def __init__(
        self,
        output_parsed: SemanticGroundednessJudgment | None,
    ) -> None:
        self.responses = FakeResponses(output_parsed)

def test_openai_semantic_evaluator_returns_supported_result():
    client = FakeOpenAI(
        SemanticGroundednessJudgment(
            is_supported=True,
            explanation="The cited evidence supports the finding.",
        )
    )

    evaluator = OpenAISemanticGroundednessEvaluator(
        client=client,
    )

    result = evaluator.evaluate(
        statement="The transaction amount was unusually high.",
        evidence_contents=[
            "The transaction triggered an alert for an unusually high amount."
        ],
    )

    assert result.is_supported is True
    assert result.explanation == (
        "The cited evidence supports the finding."
    )   

def test_openai_semantic_evaluator_returns_unsupported_result():
    client = FakeOpenAI(
        SemanticGroundednessJudgment(
            is_supported=False,
            explanation="The cited evidence does not support the finding.",
        )
    )

    evaluator = OpenAISemanticGroundednessEvaluator(
        client=client,
    )

    result = evaluator.evaluate(
        statement="The transaction amount was $500,000.",
        evidence_contents=[
            "The transaction amount was $5,000."
        ],
    )

    assert result.is_supported is False
    assert result.explanation == (
        "The cited evidence does not support the finding."
    )     

def test_openai_semantic_evaluator_rejects_missing_structured_output():
    client = FakeOpenAI(None)

    evaluator = OpenAISemanticGroundednessEvaluator(
        client=client,
    )

    with pytest.raises(
        ValueError,
        match="OpenAI returned no structured semantic groundedness judgment",
    ):
        evaluator.evaluate(
            statement="The transaction amount was unusually high.",
            evidence_contents=[
                "The transaction triggered an alert for an unusually high amount."
            ],
        )  

def test_openai_semantic_evaluator_requires_api_key(
    monkeypatch,
):
    monkeypatch.setattr(
        "api.investigation.evaluation.openai_semantic_groundedness."
        "settings.openai_api_key",
        None,
    )

    with pytest.raises(
        ValueError,
        match="OPENAI_API_KEY must be configured",
    ):
        OpenAISemanticGroundednessEvaluator()          