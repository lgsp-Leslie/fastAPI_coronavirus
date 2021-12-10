#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from datetime import datetime, date
from pathlib import Path

from pydantic import BaseModel, ValidationError, constr
from typing import List, Optional

from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base

print('\033[31m1. --- Pydantic的基本用法 ---\033[0m')


class User(BaseModel):
    id: int  # 必填字段
    name: str = 'Harold Hua'  # 有默认值，选填字段
    signup_ts: Optional[datetime] = None
    friends: List[int] = []  # 列表中元素是int类型或者可以直接转换成int类型


external_data = {
    'id': '123',
    'signup_ts': '2021-12-01 12:11',
    'friends': [1, 2, '3']
}

# python解包方式
user = User(**external_data)
print(user.id, user.friends)
print(repr(user.signup_ts))
print(user.dict())

print('\033[31m2. --- 校验失败处理 ---\033[0m')
try:
    User(id=1, signup_ts=datetime.today(), friends=['Zero', 3, 99, 'Four'])
except ValidationError as e:
    print(e.json())

print('\033[31m3. --- 模型类的属性和方法 ---\033[0m')
print(user.dict())
print(user.json())
print(user.copy())  # 浅拷贝
print(User.parse_obj(obj=external_data))  # 校验解析数据
print(User.parse_raw(
    '{"id": "123", "name": "Harold Hua", "signup_ts": "2021-10-01 12:11", "friends": [1, 2, 3]}'))  # 内层属性名称必须使用双引号

path = Path('pydantic_test.json')
path.write_text('{"id": "123", "name": "Harold Hua", "signup_ts": "2021-10-01 12:11", "friends": [1, 2, 3]}')
print(User.parse_file(path))

print(user.schema())
print(user.schema_json())

user_data = {"id": "error", "name": "Harold Hua", "signup_ts": "2021-10-01 12:11", "friends": [1, 2, 'Three']}
print(User.construct(**user_data))  # 不校验解析数据

print(User.__fields__.keys())  # 定义模型类的时候，所有字段都注明类型，字段顺序就不会乱

print('\033[31m4. --- 递归模型 ---\033[0m')


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]  # 递归模型


dogs = Dog(birthday=date.today(), weight=6.66, sound=[{'sound': 'w w~~'}, {'sound': 'y y~~'}])

print(dogs.dict())

print('\033[31m5. --- ORM模型：从类实例创建符合ORM对象的模型 ---\033[0m')

Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(95), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyMode(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=95)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True


co_orm = CompanyOrm(id=123, public_key='lgsp', name='Harold', domains=['lgsp.com', 'lgsp.cn'])

print(CompanyMode.from_orm(co_orm))
