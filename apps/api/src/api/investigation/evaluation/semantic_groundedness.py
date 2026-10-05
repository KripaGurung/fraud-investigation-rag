from dataclasses import dataclass
from typing import Protocol, runtime_checkable

@dataclass(frozen=True)
class SemanticGroundednessResult:
    """Result of checking whether a finding is supported by its cited evidence."""

    is_supported: bool
    explanation: str

@runtime_checkable
class SemanticGroundednessEvaluator(Protocol):
    """Contract for evaluating whether a finding is supported by evidence."""

    def evaluate(
        self,
        statement: str,
        evidence_contents: list[str],
    ) -> SemanticGroundednessResult:
        """Evaluate semantic support for a finding."""
            