from sqlalchemy.orm import Session
from backend_ref.repositories.models.thread import Thread
from typing import List, Optional, Type
from backend_ref.utils.date_utils import get_time_format


class ThreadRepository:
    def __init__(self, session: Session):
        self.session = session

    def CreateAutomatic(self) -> Thread:
        date_query = get_time_format()
        thread: Optional[Thread] = self.session.query(Thread).filter_by(topic=date_query).first()
        if thread is None:
            return self.Create(get_time_format())
        else:
            return thread

    def Create(self, topic: str) -> Thread:
        thread = Thread(topic=topic)
        self.session.add(thread)
        self.session.commit()
        return thread

    def LoadAll(self) -> list[Type[Thread]]:
        return self.session.query(Thread).all()
