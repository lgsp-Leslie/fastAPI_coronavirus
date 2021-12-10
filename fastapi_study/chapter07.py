#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from fastapi import APIRouter, Depends, Request


async def get_user_agent(request: Request):
    print(request.headers['User-Agent'])


app07 = APIRouter(
    prefix='/bigger_applications',
    tags=[''],
    dependencies=[Depends(get_user_agent)],
    responses={200: {'description': 'Good'}}
)


@app07.get('/bigger_application')
async def bigger_application():
    return {'message': 'Bigger applications - Multiple files'}
