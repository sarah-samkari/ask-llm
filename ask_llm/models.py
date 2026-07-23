from pydantic import BaseModel, Field


class Answer(BaseModel):
    """A structured, validated answer returned by the LLM."""

    question: str = Field(..., description="The original question that was asked.")
    answer: str = Field(..., description="A direct, concise answer to the question.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence from 0.0 to 1.0.")
    reasoning: str = Field(default="", description="A short explanation of the answer.")
    sources: list = Field(default_factory=list, description="Any sources or caveats.")