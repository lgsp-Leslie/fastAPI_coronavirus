#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from sqlalchemy.orm import Session

from coronavirus import schemas
from coronavirus.models import City, Data


def get_city(db: Session, city_id: id):
    return db.query(City).get(city_id)


def get_city_by_name(db: Session, name: str):
    return db.query(City).filter_by(province=name).first()


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CreateCity):
    db_city = City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_data(db: Session, city: str = None, skip: int = 0, limit: int = 10):
    if city:
        return db.query(Data).filter(Data.city.has(province=city)).all()
    return db.query(Data).offset(skip).limit(limit).all()


def create_city_data(db: Session, data: schemas.CreateData, city_id: int):
    db_data = Data(**data.dict(), city_id=city_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
