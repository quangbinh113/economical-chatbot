from pydantic import BaseModel
from typing import Optional


class Create_history_rq(BaseModel):
    question: str
    answer: str


class Answer_click(BaseModel):
    Content: str
    Metadata: Optional[dict] = None


class save_click(BaseModel):
    question: str
    answer: Answer_click

    def addAnswer(self, ans: Answer_click):
        self.answer = ans
