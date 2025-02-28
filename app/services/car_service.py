from app.models import Car, ClearanceEnum, DriveEnum, TyreEnum, BodyType, Tag
from app.services.helpers import add_and_get_body_types, add_and_get_tags
from app.data.db_setup import SessionLocal

# Create a session
session = SessionLocal()


def add_car(
    brand: str,
    model: str,
    year: int,
    car_class: str,
    rq: int,
    has_abs: bool,
    has_tcs: bool,
    clearance: ClearanceEnum,
    tyre: TyreEnum,
    country: str,
    drive: DriveEnum,
    fuel: str,
    seats: int,
    engine_placement: str,
    brake: str,
    rid: str,
    body_types: list[str],
    tags: list[str],
    tune: str
) -> None:
    """Add a car to the database."""

    body_types = add_and_get_body_types(body_types)
    tags = add_and_get_tags(tags)

    new_car = Car(
        brand=brand,
        model=model,
        year=year,
        car_class=car_class,
        rq=rq,
        has_abs=has_abs,
        has_tcs=has_tcs,
        clearance=clearance,
        tyre=tyre,
        country=country,
        drive=drive,
        fuel=fuel,
        seats=seats,
        engine_placement=engine_placement,
        brake=brake,
        rid=rid,
        body_types=body_types,
        tags=tags,
        tune=tune
    )
    session.merge(new_car)
    session.commit()


def get_all_cars():
    return session.query(Car).all()


def get_car_by_id(car_id):
    return session.query(Car).filter(Car.car_id == car_id).first()


def delete_car(car_id):
    car = get_car_by_id(car_id)
    if car:
        session.delete(car)
        session.commit()
        print(f"Deleted car: {car.model}")


def update_car_tune(car_id, new_tune):
    car = get_car_by_id(car_id)
    if car:
        car.tune = new_tune
        session.commit()
        print(f"Updated car tune: {car.model} to {new_tune}")
