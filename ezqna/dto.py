from pydantic import BaseModel, Field


class CreateQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=280)
    anonymous: bool = Field(default=False)


class AnswerQuestion(BaseModel):
    answer: str = Field(min_length=1, max_length=280)
