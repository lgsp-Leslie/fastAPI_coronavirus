#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
import time

import uvicorn

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from coronavirus import application as app07_application
from fastapi_study import app03, app04, app05, app06, app07, app08

# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import PlainTextResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException

# app = FastAPI()

# FastAPI应用常见配置项
from fastapi_study.chapter05 import verify_token, verify_key

app = FastAPI(
    title='FastAPI API Docs Title',
    description='FastAPI 接口文档描述',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redocs',
    # dependencies=[Depends(verify_token), Depends(verify_key)]  # FastAPI框架中全局依赖的使用(方法2),方法1见chapter05.py
)

# FastAPI项目的静态文件配置
app.mount(path='/static', app=StaticFiles(directory='./coronavirus/static'), name='static')


# FastAPI Handling Errors错误处理
# @app.exception_handler(StarletteHTTPException)  # 重写HTTPException异常处理器
# async def http_exception_handler(request, exc):
#     """
#     :param request: 必填
#     :param exc:
#     :return:
#     """
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
#
# @app.exception_handler(RequestValidationError)  # 重写请求验证异常处理器
# async def validation_exception_handle(request, exc):
#     """
#     :param request: 必填
#     :param exc:
#     :return:
#     """
#     return PlainTextResponse(str(exc), status_code=400)


# Middleware中间件
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):  # call_next将接收request请求作为参数
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-process-Time'] = str(process_time)  # 添加自定义以‘X-’开头的请求头
    return response


# 跨域处理
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://127.0.0.1',
        'http://127.0.0.1:8080',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(app03, prefix='/c03', tags=['第三章，请求参数和验证'])
app.include_router(app04, prefix='/c04', tags=['第四章，响应处理和Fast API配置'])
app.include_router(app05, prefix='/c05', tags=['第五章，FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/c06', tags=['第六章，安全、认证和授权'])
app.include_router(app07, prefix='/c07', tags=['第七章，FastAPI的数据库操作和多应用的目录结构设计'])
app.include_router(app07_application, prefix='/coronavirus', tags=['新冠病毒疫情跟踪器API'])
app.include_router(app08, prefix='/c08', tags=['第八章，FastAPI中间件、CORS、后台任务、测试用例'])

if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=81, reload=True, debug=True, workers=8)


# 带yield的依赖,py3.7以上支持,py3.6需安装async-exit-stack、async-generator
# 以下是伪代码
async def get_db():
    db = 'db_connection'
    try:
        yield db
    finally:
        db.endswith('db_close')


async def dependency_a():
    dep_a = 'generate_dep_a()'
    try:
        yield dep_a
    finally:
        dep_a.endswith('db_close')


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = 'generate_dep_b()'
    try:
        yield dep_b
    finally:
        dep_b.endswith(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = 'generate_dep_c()'
    try:
        yield dep_c
    finally:
        dep_c.endswith(dep_b)
