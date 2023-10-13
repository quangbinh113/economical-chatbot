from typing import List
from pydantic import BaseModel


class Qa(BaseModel):
    Question: str
    Answer: Answer

    def AddAnswer(self, Ansr: Answer):
        self.Answer = Ansr


class Answer(BaseModel):
    Content: str
    Metadata: dict


class ThreadQA(BaseModel):
    QaList: List[Qa]

    def AppendQa(self, qa: Qa):
        self.QaList.append(qa)

    def Get(self) -> List[Qa]:
        return self.QaList
