#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
import datetime
from enum import Enum
from typing import Optional, List

from fastapi import APIRouter, Path, Query, Cookie, Header
from pydantic import BaseModel, Field

app03 = APIRouter()


@app03.get('/path/parameters')
def path_params01():
    return {'msg': 'This is a message!'}


@app03.get('/path/{parameters}')
def path_params01(parameters: str):
    return {'msg': parameters}


class CityName(str, Enum):
    Beijing = 'Beijing China'
    Shanghai = 'Shanghai China'


# 枚举类型参数
@app03.get('/enum/{city}')
async def latest(city: CityName):
    if city == CityName.Beijing:
        return {'City Name': city, 'confirmed': 1492, 'death': 7}
    if city == CityName.Shanghai:
        return {'City Name': city, 'confirmed': 492, 'death': 7}

    return {'City Name': city, 'latest': 'unknown'}


# 通过path parameters传递文件路径
@app03.get('/files/{file_path:path}')
def filepath(file_path: str):
    return f'The file path is {file_path}'


# 校验数字
@app03.get('/path_num/{num}')
def path_params_validate(
        num: int = Path(..., title='Your number', description='描述信息', ge=1, le=10)
):
    return num


# 查询参数和字符串验证
# 给了默认值就是选填参数
@app03.get('/query')
def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {'page': page, 'limit': limit}
    return {'page': page}


# bool类型转换：yes、on、1、True、true
@app03.get('/query/bool/conversion')
def type_conversion(param: bool = False):
    return param


# 多个查询参数的列表，参数别名
@app03.get('/query/validations')
def query_params_validate(
        value: str = Query(..., min_length=8, max_length=16, regex='^a'),
        values: List[str] = Query(default=['v1', 'v2'], alias='alias_name')
):
    return value, values


# 请求体和字段
class CityInfo(BaseModel):
    name: str = Field(..., example='Beijing')
    country: str
    country_code: str = None
    country_population: int = Field(default=800, title='人口数量', description='国家的人口数量', ge=800)

    class Config:
        schema_extra = {
            'example': {
                'name': 'Shanghai',
                'country': 'China',
                'country_code': 'CN',
                'country_population': 1400000000,
            }
        }


@app03.post('/request_body/city')
def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.dict()


# 多参数（Req Body、params PATH、p Query）混合
@app03.put('/request_body/city/{name}')
def mix_city_info(
        name: str,
        city01: CityInfo,
        city02: CityInfo,  # Request Body可以定义多个
        confirmed: int = Query(ge=0, description='确诊数', default=0),
        deaths: int = Query(ge=0, description='死亡数', default=0)
):
    if name == 'Shanghai':
        return {name: {'confirmed': confirmed, 'death': deaths}}
    return city01.dict(), city02.dict()


# 定义数据格式嵌套的请求体
class Data(BaseModel):
    city: List[CityInfo] = None  # 定义数据格式嵌套的请求体
    date: datetime.date
    confirmed: int = Field(ge=0, description='确诊数', default=0)
    deaths: int = Field(ge=0, description='死亡数', default=0)
    recovered: int = Field(ge=0, description='痊愈数', default=0)


@app03.put('/request_body/nested')
def nested_models(data: Data):
    return data


# 设置Cookie和Header参数
@app03.get('/cookie')
def cookie(cookie_id: Optional[str] = Cookie(None)):  # 定义Cookie参数需要使用Cookie类
    return {'cookie_id': cookie_id}


@app03.get('/header')
def header(user_agent: Optional[str] = Header(None, convert_underscores=True), x_token: List[str] = Header(None)):
    """
    有些HTTP代理和服务器是不允许在请求头中带有下划线的，所以Header提供convert_underscores属性进行转换（-）设置
    :param user_agent: convert_underscores=True 会把user_agent 变成user-agent
    :param x_token: 包含多个值的列表
    :return:
    """
    return {'User-Agent': user_agent, 'x-token': x_token}
