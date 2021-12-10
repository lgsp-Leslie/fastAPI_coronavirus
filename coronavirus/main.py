#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from coronavirus import schemas, crud
from coronavirus.database import Base, engine, SessionLocal
from coronavirus.models import City, Data

application = APIRouter()

templates = Jinja2Templates(directory='./coronavirus/templates')

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@application.post('/create_city', response_model=schemas.ReadCity)
def create_city(city: schemas.CreateCity, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city.province)
    if db_city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='城市已经存在')
    return crud.create_city(db=db, city=city)


@application.get('/get_city/{city}', response_model=schemas.ReadCity)
def get_city(city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='城市不存在')
    return db_city


@application.get('/get_cities', response_model=List[schemas.ReadCity])
def get_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db, skip=skip, limit=limit)
    return cities


@application.post('/create_data', response_model=schemas.ReadData)
def create_data_for_city(city: str, data: schemas.CreateData, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    print(db_city)
    if db_city is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='城市不存在')
    data = crud.create_city_data(db=db, data=data, city_id=db_city.id)
    return data


@application.get('/get_data')
def get_data(city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    return data


def bg_task(url: HttpUrl, db: Session):
    # 不要在后台任务的参数中db: Session = Depends(get_db)这样导入依赖，先在外部导入依赖后再传过来
    city_data = requests.get(url=f'{url}?source=jhu&country_code=CN&timelines=false')

    if city_data.status_code == 200:
        db.query(City).delete()
        for item in city_data.json()['locations']:
            city = {
                'province': item['province'],
                'country': item['country'],
                'country_code': 'CN',
                'country_population': item['country_population']
            }
            # crud.create_city(db=db, city=schemas.CreateCity(**city))
            print(city=schemas.CreateCity(**city))

    coronavirus_data = requests.get(url=f'{url}?source=jhu&country_code=CN&timelines=true')

    if 200 == city_data.status_code:
        db.query(Data).delete()
        for item in coronavirus_data.json()['locations']:
            db_city = crud.get_city_by_name(db=db, name=item["province"])
            print('db_city', db_city)
            for date, confirmed in item['timelines']['confirmed']['timeline'].items():
                data = {
                    'date': date.split('T')[0],
                    'confirmed': confirmed,
                    'deaths': item['timelines']['deaths']['timeline'][date],
                    'recovered': 0,
                }
                # crud.create_city_data(db=db, data=schemas.CreateData(**data), city_id=db_city.id)
                print('')


@application.get('/sync_coronavirus_data/jhu')
def sync_coronavirus_data(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(bg_task, 'https://coronavirus-tracker-api.herokuapp.com/v2/locations', db)
    return {'message': '正在返回数据'}


@application.get('/')
def coronavirus(request: Request, city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    return templates.TemplateResponse('home.html', {
        'request': request,
        'data': data,
        'sync_data_url': '/coronavirus/sync_coronavirus_data/jhu'
    })
