from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from app.data.db_setup import Base

class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String(255), nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    event_dir = Column(String(255), nullable=False)
    ended = Column(Boolean, default=False)
