from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from app.data.db_setup import Base

class ClubTrackSet(Base):
    __tablename__ = "club_track_set"

    club_set_id = Column(Integer, primary_key=True, autoincrement=True)
    track_set_name = Column(String(255), nullable=False)
    active = Column(Boolean, default=False)

class ClubReq(Base):
    __tablename__ = "club_reqs"

    club_req_id = Column(Integer, primary_key=True, autoincrement=True)
    req = Column(String(255))
    req_number = Column(Integer)
    time_added = Column(TIMESTAMP, nullable=False)

class ClubEvent(Base):
    __tablename__ = "club_event"

    club_id = Column(Integer, primary_key=True, autoincrement=True)
    club_name = Column(String(255), nullable=False)
    played_matches = Column(Integer, default=1)
    ended = Column(Boolean, default=False)
    rq = Column(Integer, nullable=False)
    club_set_id = Column(Integer, ForeignKey("club_track_set.club_set_id", ondelete="CASCADE"))
    club_req1_id = Column(Integer, ForeignKey("club_reqs.club_req_id", ondelete="CASCADE"))
    club_req2_id = Column(Integer, ForeignKey("club_reqs.club_req_id", ondelete="CASCADE"))
