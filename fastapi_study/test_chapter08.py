#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from run import app


app.mount(path='/static', app=StaticFiles(directory='../coronavirus/static'), name='static')
# Testing 测试用例
client = TestClient(app)


def test_run_bg_task():  # 函数名用test_开头，pytest的规范，不能使用async def
    response = client.post(url='/c08/background_tasks?framework=FastAPI')
    assert response.status_code == 200
    assert response.json() == {'message': '任务已在后台运行！'}


def test_dependency_run_bg_task():
    response = client.post(url="/c08/dependency/background_tasks")
    assert response.status_code == 200
    assert response.json() is None


def test_dependency_run_bg_task_q():
    response = client.post(url="/c08/dependency/background_tasks?q=1")
    assert response.status_code == 200
    assert response.json() == {'message': '任务已在后台运行！'}
