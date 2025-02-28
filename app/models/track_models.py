from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.data.db_setup import Base

class TrackSet(Base):
    __tablename__ = "track_set"

    track_set_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=True)

class TrackSerie(Base):
    __tablename__ = "track_serie"

    track_serie_id = Column(Integer, primary_key=True, autoincrement=True)
    serie_number = Column(Integer, nullable=False)
    track_set_id = Column(Integer, ForeignKey("track_set.track_set_id", ondelete="CASCADE"))

class Race(Base):
    __tablename__ = "races"

    race_id = Column(Integer, primary_key=True, autoincrement=True)
    race_name = Column(String(255), nullable=False)
    road_type = Column(String(255), nullable=False)
    conditions = Column(JSON)  # Storing conditions as JSON
    race_number = Column(Integer, nullable=False)
    track_serie_id = Column(Integer, ForeignKey("track_serie.track_serie_id", ondelete="CASCADE"))


class CarAssignment(Base):
    __tablename__ = "car_assignments"

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey("races.race_id", ondelete="CASCADE"))
    car_number = Column(Integer, nullable=False)
