# models/book.py
from sqlalchemy import Column, Integer, String, DateTime, func, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from backend_ref.config import base


class Thread(base):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    histories = relationship('History', back_populates='thread')  # One-to-Many relationship

