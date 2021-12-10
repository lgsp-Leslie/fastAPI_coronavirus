#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from typing import Optional

from fastapi import APIRouter, Depends, BackgroundTasks

app08 = APIRouter()


# Middleware中间件==>run.py

# 带yield的依赖的退出部分的代码和后台任务，会在中间件之后运行

# 跨域处理==>run.py

# 后台任务
@app08.post('/background_tasks')
async def run_bg_task(framework: str, background_tasks: BackgroundTasks):
    """

    :param framework: 被调用的后台任务函数的参数
    :param background_tasks:
    :return:
    """
    background_tasks.add_task(bg_task, framework)
    return {'message': '任务已在后台运行！'}


def bg_task(framework: str):
    with open('README.md', mode='a') as f:
        f.write(f'## {framework} 后台任务')


# 通过依赖使用后台任务
def continue_write_readme(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        background_tasks.add_task(bg_task, '\n>通过依赖使用后台任务\n')
    return q


@app08.post('/dependency/background_tasks')
async def dependency_run_bg_task(q: str = Depends(continue_write_readme)):
    if q:
        return {'message': '任务已在后台运行！'}



