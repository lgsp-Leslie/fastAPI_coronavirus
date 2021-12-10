#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException

app05 = APIRouter()


# 创建、导入和声明依赖
# 函数作为依赖项
async def common_parameters(q: Optional[str] = None, page: int = 1, limit: int = 100):
    return {'q': q, 'page': page, 'limit': limit}


@app05.get('/dependency01')
async def dependency01(commons: dict = Depends(common_parameters)):
    return commons


@app05.get('/dependency02')
def dependency02(commons: dict = Depends(common_parameters)):
    return commons


# 类作为依赖项
fake_items_db = [{'item_name': '1'}, {'item_name': '2'}, {'item_name': '3'}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, page: int = 1, limit: int = 100):
        self.q = q
        self.page = page
        self.limit = limit


@app05.get('/classes_as_dependencies')
# async def classes_as_dependencies(commons: CommonQueryParams = Depends(CommonQueryParams)):
# async def classes_as_dependencies(commons: CommonQueryParams = Depends()):
async def classes_as_dependencies(commons=Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({'q': commons.q})

    items = fake_items_db[commons.page: commons.page + commons.limit]
    response.update({'items': items})
    return response


# 子依赖
def query(q: Optional[str] = None):
    return q


def sub_query(q: str = Depends(query), last_query: Optional[str] = None):
    if not q:
        return last_query
    return q


@app05.get('/sub_dependency')
async def sub_dependency(final_query: str = Depends(sub_query, use_cache=True)):
    # use_cache为True,表示当多个依赖有一个共同的子依赖时,每次request请求只会调用子依赖一次,多次调用将从缓存中获取
    return {'sub_dependency': final_query}


# 路径操作装饰器中的多依赖
async def verify_token(x_token: str = Header(...)):
    # 没有返回值的子依赖
    if x_token != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')
    return x_token


async def verify_key(x_key: str = Header(...)):
    # 有返回值的子依赖,但是返回值不会被调用
    if x_key != 'fake-super-secret-key':
        raise HTTPException(status_code=400, detail='X-Key header invalid')
    return x_key


@app05.get('/dependency_in_path_operation', dependencies=[Depends(verify_token), Depends(verify_key)])
async def dependency_in_path_operation():
    return [{'user': 'user01'}, {'user': 'user02'}]


# FastAPI框架中全局依赖的使用(方法1)
# app05 = APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)])
