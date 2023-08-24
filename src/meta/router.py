# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 15:32 2023/8/11
# @Description: 元数据路由
# @Version: Python 3.8.11
# @Modified By:
import sqlalchemy
from fastapi import APIRouter
from sqlalchemy.exc import InvalidRequestError

from src.meta.models import QueryEntities
from src.meta.service import MetaService
from src.models import NormalResponse, FailureResponse

router = APIRouter()
meta = MetaService()


@router.get("/api/v1/ids3/meta/sources", summary="更新数据源信息", deprecated=False,
            description="主要用于更新数据源的信息")
async def get_sources():
    try:
        result = meta.list_sources(start=0, count=10)
        return NormalResponse(msg="数据源列表", data=result)
    except AttributeError as e:
        return NormalResponse(code=500, msg="解析属性或方法时发生了错误", data=e)
    except InvalidRequestError as e:
        return NormalResponse(code=500, msg="数据校验有误", data=e)
    except Exception as e:
        print(type(e))
        return FailureResponse(code=500, msg="发生了未知错误", data=None)


@router.post("/api/v1/ids3/meta/entity", summary="展示元数据实体", deprecated=False)
def list_entities(model: QueryEntities):
    try:
        result = meta.list_entities(model.entity_type, model.keyword, model.start, model.count)
        return NormalResponse(msg="元数据实体列表", data=result)
    except AttributeError:
        return FailureResponse(code=500, msg="属性或方法时发生了错误", data=None)
    except KeyError:
        return FailureResponse(code=500, msg="输入 entity_type 参数有误", data=None)
    except Exception as e:
        print(type(e))
        return FailureResponse(code=500, msg="发生了未知错误", data=None)
