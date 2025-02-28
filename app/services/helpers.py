from app.data.db_setup import SessionLocal
from app.models.car_models import BodyType, Tag
from config import logger
session = SessionLocal()

def get_body_type_id(body_type_name):
    body_type = session.query(BodyType).filter(BodyType.body_type_name == body_type_name).first()
    return body_type.body_type_id if body_type else None

def add_body_type(body_type_name):
    body_type_id = get_body_type_id(body_type_name)
    if body_type_id:
        logger.debug(f"Body type {body_type_name} already exists with id {body_type_id}")
    else:
        new_body_type = BodyType(body_type_name=body_type_name)
        session.add(new_body_type)
        session.commit()

def add_and_get_body_types(body_type_names: list[str]):
    for body_type_name in body_type_names:
        add_body_type(body_type_name)
    body_types = session.query(BodyType).filter(BodyType.body_type_name.in_(body_type_names)).all()
    return body_types

def get_tag_id(tag_name):
    tag = session.query(Tag).filter(Tag.tag_name == tag_name).first()
    return tag.tag_id if tag else None


def add_tag(tag_name):
    tag_id = get_tag_id(tag_name)
    if tag_id:
        logger.debug(f"Tag {tag_name} already exists with id {tag_id}")
    else:
        new_tag = Tag(tag_name=tag_name)
        session.add(new_tag)
        session.commit()

def add_and_get_tags(tag_names: list[str]):
    for tag_name in tag_names:
        add_tag(tag_name)
    tags = session.query(Tag).filter(Tag.tag_name.in_(tag_names)).all()
    return tags
