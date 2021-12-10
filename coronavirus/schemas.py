#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
import datetime

from pydantic import BaseModel


class CreateData(BaseModel):
    date: datetime.date
    confirmed: int = 0
    deaths: int = 0
    recovered: int = 0


class CreateCity(BaseModel):
    country: str
    country_code: str
    country_population: str
    province: str


class ReadData(CreateData):
    id: int
    city_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class ReadCity(CreateCity):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
