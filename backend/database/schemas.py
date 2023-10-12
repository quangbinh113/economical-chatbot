from pydantic import BaseModel
from typing import Optional
import datetime


class AIResponseModel(BaseModel):
    response: Optional[str]


class AIQueryModel(BaseModel):
    question: str


class CreateHistoryRequest(BaseModel):
    question: str
    answer: str


class AnswerClickResponse(BaseModel):
    Content: str
    Metadata: Optional[dict] = None


class SaveClickResponse(BaseModel):
    question: str
    answer: AnswerClickResponse

    def add_answer(self, ans: AnswerClickResponse):
        self.answer = ans


class CreateHistoryResponse(BaseModel):
    question: str
    answer: str
    location_html: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    title: str
    topic: str


class ThreadItem(BaseModel):
    id: int
    updated_at: datetime.datetime
    created_at: datetime.datetime
    topic: str