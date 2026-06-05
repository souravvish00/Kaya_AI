from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    mode: str = "assistant"
    save_training: bool = False


class ChatResponse(BaseModel):
    response: str
    session_id: str
    mode: str


class TrainingExample(BaseModel):
    prompt: str = Field(min_length=1)
    completion: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)
    rating: int = Field(default=5, ge=1, le=5)


class TrainingJobRequest(BaseModel):
    model_name: str = "Qwen/Qwen3-8B"
    method: str = "lora"
    epochs: int = Field(default=3, ge=1, le=50)
    learning_rate: float = Field(default=0.0002, gt=0)


class CalculatorRequest(BaseModel):
    expression: str = Field(min_length=1)
