from pydantic import BaseModel
import datetime
from typing import Optional


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
