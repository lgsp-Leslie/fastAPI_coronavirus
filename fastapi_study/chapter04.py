#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from typing import Optional, Union, List

from fastapi import APIRouter, Form, File, UploadFile, HTTPException, status
from pydantic import BaseModel, EmailStr

app04 = APIRouter()


# 响应模型
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    mobile: str = '10086'
    address: str = None
    full_name: Optional[str] = None


class UserIn(BaseUser):
    password: str


class UserOut(BaseUser):
    pass


users = {
    'user01': {'username': 'user01', 'password': '123', 'email': 'user01@qq.com'},
    'user02': {'username': 'user02', 'password': '123', 'email': 'user02@qq.com', 'mobile': '9999'},
}


# path operation
@app04.post('/response_model', response_model=UserOut,
            response_model_exclude_unset=True)  # response_model_exclude_unset=True表示默认值不包含在响应中
async def response_model(user: UserIn):
    print(user.password)
    return users['user01']
    # return users['user02']


@app04.post(
    '/response_model/attributes',
    response_model=UserOut,
    # response_model=Union[UserIn, UserOut],   # Union并集
    # response_model=List[UserOut]      # return [user1, user2]
    # response_model_include=['username', 'email'],    # 包含
    # response_model_exclude = ['mobile'],      # 排除
)
async def response_model_attributes(user: UserIn):
    # del user.password     # Union[UserIn, UserOut]后，删除password属性返回
    return user


# 响应状态码和快捷属性
@app04.post('/status_code', status_code=200)
async def status_code():
    return {'status_code': 200}


@app04.post('/status_attribute', status_code=status.HTTP_200_OK)
async def status_attribute():
    print(type(status.HTTP_200_OK))
    return {'status_code': status.HTTP_200_OK}


# 表单数据处理
@app04.post('/login')
async def login(username: str = Form(...), password: str = Form(...)):
    return {'username': username}


# 单文件、多文件上传及参数详解
@app04.post('/file1')
async def file_1(file: bytes = File(...)):
    # File类，文件内容以bytes的形式读入内存，适合上传小文件
    return {'file_size', len(file)}


@app04.post('/file2')
async def file_2(files: List[bytes] = File(...)):
    # File类，文件内容以bytes的形式读入内存，适合上传小文件
    size = []
    for item in files:
        size.append(len(item))
    return size


@app04.post('/upload_files1')
async def upload_files(file: UploadFile = File(...)):
    # UploadFile，文件存储在内存中，使用的内存达到阈值后，将被保存到磁盘中；
    # 适合上传图片、视频；
    # 可以获取上传的文件的元数据，如文件名，创建时间等；
    # 有文件对象的异步接口；上传的文件是python文件对象，可以使用write(),read(),seek(),close()操作；

    return {'filename': file.filename}


@app04.post('/upload_files2')
async def upload_files(files: List[UploadFile] = File(...)):
    for item in files:
        contents = await item.read()
        # print(contents)
    return {'filename': files[0].filename, 'content_type': files[0].content_type}


# FastAPI项目的静态文件配置==>run.py

# 路径操作配置
@app04.post(
    '/path_operation_configuration',
    response_model=UserOut,
    # tags=['Path', 'Operation', 'Configuration'],
    summary='This is summary',
    description='This is description',
    response_description='This is response_description',
    # deprecated=True,  # 废弃接口
    status_code=status.HTTP_200_OK
)
async def path_operation_configuration(user: UserIn):
    """
    Path Operation Configuration 路径操作配置
    :param user: 用户信息
    :return: 返回结果
    """
    return user.dict()


# FastAPI应用常见配置项==>run.py


# FastAPI Handling Errors错误处理==>run.py
# HTTPException 错误处理
@app04.get('/http_exception')
async def http_exception(city: str):
    if city != ' Beijing':
        raise HTTPException(status_code=404, detail='City ' + city + 'not found!', headers={'X-Error': 'Error'})

    return {'city': city}


@app04.get('/http_exception/{city_id}')
async def override_http_exception(city_id: int):
    if city_id == 1:
        raise HTTPException(status_code=418, detail='Nope! I don’t like 1.')

    return {'city_id': city_id}
