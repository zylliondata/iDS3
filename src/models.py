# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 10:05 2023/8/8
# @Description: 通用的模型封装
# @Version: Python 3.8.11
# @Modified By:
from pydantic import BaseModel


class NormalResponse(BaseModel):
    code: int = 200
    msg: str = "active"
    # result: List[List[Tuple]] = []
    data: object


class FailureResponse(BaseModel):
    code: int = -1
    msg: str = "failure"
    data: None
