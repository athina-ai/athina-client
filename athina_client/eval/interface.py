from abc import abstractmethod
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# These classes are equivalent to the ones in the stdllm package
class EvalResultMetric(BaseModel):
    """
    Represents the LLM evaluation result metric.
    """

    id: str
    value: float


class EvalResult(BaseModel):
    """
    Represents the LLM evaluation result.
    """

    name: str
    display_name: str
    score: float
    passed: bool
    explanation: str
    runtime: int  # in milliseconds
    metrics: List[EvalResultMetric] = Field(default_factory=list)


class Eval(BaseModel):
    """
    Base class for evaluation.
    """

    name: str
    display_name: str
    description: Optional[str] = None

    def to_config(self) -> Optional[Dict[str, Any]]:
        """
        Convert the evaluation to a portable config.
        """
        return None

    @abstractmethod
    def evaluate(self, **kwargs) -> EvalResult:
        pass
