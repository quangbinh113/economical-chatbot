from sqlalchemy.orm import Session
from backend_ref.repositories.models.history import History
from backend_ref.repositories.models.thread import Thread
from typing import Optional

from typing import List
from backend_ref.utils.date_utils import get_time_format


class HistoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def Create(self, message, answer, title, time_response) -> History:
        historyModel = History(message=message, title=title, time_response=time_response, answer=answer)
        self.session.add(historyModel)
        self.session.commit()
        return historyModel

    def LoadAll(self) -> List[History]:
        return self.session.query(History).all()

    def auto_fill_qa(self, message: str, answer: str):
        date_query: str = get_time_format()
        thread: Optional[Thread] = self.session.query(Thread).filter_by(topic=date_query).first()
        if thread is None:
            raise Exception("thread not found, create first")

        history = History(message=message, answer=answer, title=date_query, time_response=0.17, thread=thread)
        self.session.add(history)
        self.session.commit()
        return history

    def loadALlbyThread(self, topic: str):
        thread: Optional[Thread] = self.session.query(Thread).filter_by(topic=topic).first()
        if thread is None:
            raise Exception("thread not found, create first")
        else:
            # filtered_records = self.session.query(History).filter(History.thread_id== thread.id).all()
            return thread.histories
