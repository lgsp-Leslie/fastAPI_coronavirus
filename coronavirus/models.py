#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, func, ForeignKey, Date
from sqlalchemy.orm import relationship

from coronavirus.database import Base


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False, comment='国家')
    country_code = Column(String(10), nullable=False, comment='国家代码')
    country_population = Column(BigInteger, nullable=False, comment='国家人口')
    province = Column(String(100), unique=True, nullable=False, comment='省/直辖市')
    data = relationship('Data', back_populates='city')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper__args__ = {'order_by': country_code}

    def __repr__(self):
        return f'{self.country}_{self.province}'


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), comment='所属省/直辖市')
    date = Column(Date, nullable=False, comment='数据日期')
    confirmed = Column(BigInteger, default=0, comment='确诊数量')
    deaths = Column(BigInteger, default=0, comment='死亡数量')
    recovered = Column(BigInteger, default=0, comment='痊愈数量')

    city = relationship('City', back_populates='data')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper__args__ = {'order_by': date.desc()}

    def __repr__(self):
        return f'{repr(self.date)}：确诊{self.confirmed}例!'
