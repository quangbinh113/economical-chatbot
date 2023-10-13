from pydantic import BaseModel
from typing import Optional


class CreateHistoryRequest(BaseModel):
    question: str
    answer: str


class AnswerClickReponse(BaseModel):
    content: str
    metadata: Optional[dict] = None


class SaveClickResponse(BaseModel):
    question: str
    answer: AnswerClickReponse
    
    def add_answer(self, ans: AnswerClickReponse):
        self.answer = ans
