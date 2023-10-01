from pydantic import BaseModel

class Create_history_rq(BaseModel):
    question:str
    answer: str