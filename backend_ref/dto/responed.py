from pydantic import BaseModel
import datetime

class Create_history_response(BaseModel):
    question:str
    answer: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    title: str
    topic :str