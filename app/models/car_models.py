from sqlalchemy import ForeignKey,Column, Integer, String, Boolean, Enum, Table
from sqlalchemy.orm import relationship
from app.data.db_setup import Base
from enum import Enum as PyEnum


# Join table for Many-to-Many relationship between Cars and Tags
car_tags = Table(
    "car_tags", Base.metadata,
    Column("car_id", Integer, ForeignKey("cars.car_id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True)
)

car_body_types = Table(
    "car_body_types", Base.metadata,
    Column("car_id", Integer, ForeignKey("cars.car_id", ondelete="CASCADE"), primary_key=True),
    Column("body_type_id", Integer, ForeignKey("body_types.body_type_id", ondelete="CASCADE"), primary_key=True)
)

class BodyType(Base):
    __tablename__ = "body_types"

    body_type_id = Column(Integer, primary_key=True, autoincrement=True)
    body_type_name = Column(String(255), nullable=False)


class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String(255), nullable=False)



class ClearanceEnum(str, PyEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class DriveEnum(str, PyEnum):
    FWD = "FWD"
    RWD = "RWD"
    AWD = "4WD"
    
class TyreEnum(str, PyEnum):
    ALL_SURFACE = "All-Surface"
    OFF_ROAD = "Off-Road"
    PERFORMANCE = "Performance"
    SLICK = "Slick"
    STANDARD = "Standard"

class Car(Base):
    __tablename__ = "cars"

    car_id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    car_class = Column(String(1), nullable=False)
    rq = Column(Integer, nullable=False)
    has_abs = Column(Boolean, nullable=False)
    has_tcs = Column(Boolean, nullable=False)
    clearance = Column(Enum(ClearanceEnum, native_enum=False), nullable=False, default=ClearanceEnum.MEDIUM)  
    tyre = Column(Enum(TyreEnum, native_enum=False), nullable=False, default=TyreEnum.STANDARD)
    country = Column(String(2), nullable=False)
    drive = Column(Enum(DriveEnum, native_enum=False), nullable=False)
    fuel = Column(String(25), nullable=False)
    seats = Column(Integer, nullable=False)
    engine_placement = Column(String(25), nullable=False)
    brake = Column(String(1), nullable=False)
    rid = Column(String(255), nullable=False)
    # Many-to-Many Relationship
    tags = relationship("Tag", secondary=car_tags, backref="cars")
    body_types = relationship("BodyType", secondary=car_body_types, backref="cars")
    
    tune = Column(String(3), default="000")

