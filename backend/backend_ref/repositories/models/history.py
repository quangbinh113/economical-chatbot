# models/book.py
from sqlalchemy import Column, Integer,ForeignKey, String, DateTime, func, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from backend_ref.config import base


class History(base):
    __tablename__ = 'histories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    location_html = Column(String, nullable=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    time_response = Column(Float)
    thread_id = Column(Integer, ForeignKey('threads.id'))  # Foreign key relationship

    thread = relationship('Thread', back_populates='histories')

