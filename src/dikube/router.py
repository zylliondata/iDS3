# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 9:35 2023/8/10
# @Description: DIKube Router
# @Version: Python 3.8.11
# @Modified By:
import uuid
from datetime import datetime

from fastapi import APIRouter, Query

from src.database.models import DIKube
from src.dikube.models import RequestDIKubeModel
from src.dikube.service import DIKubeService
from src.models import NormalResponse

router = APIRouter()

dikube = DIKubeService()


@router.get("/api/v1/ids3/dikube", summary="DIKube 分页查询", deprecated=False)
def list_dikube(
        page_number: int = Query(title="当前页", default=1, ge=1, description="当前页码"),
        page_size: int = Query(title="分页大小", default=10, ge=1, le=1000, description="分页大小范围1-1000"),
        project: str = Query(title="项目", default="catalog", description="项目", min_length=3, max_length=50)
):
    if project not in ["catalog", "dikube"]:
        return NormalResponse(code=400, msg="project 参数错误,[catalog|dikube]", data=None)
    try:
        result = dikube.query_dikube_by_page(project=project, page_number=page_number, page_size=page_size)
        return NormalResponse(msg="查询成功", data=result)
    except Exception as e:
        return NormalResponse(code=500, msg="查询失败", data=str(e))


@router.post("/api/v1/ids3/dikube", summary="DIKube 记录创建", deprecated=False)
def create_dikube(model: RequestDIKubeModel):
    dikube_model = model.dict()
    dikube_model['id'] = str(uuid.uuid4())
    dikube_model['createdAt'] = datetime.utcnow()
    # dikube_model['updatedAt'] = datetime.now()
    dikube_model['status'] = True
    dikube.create_dikube(DIKube(**dikube_model))
    return NormalResponse(msg="创建成功", data=dikube_model['id'])


@router.put("/api/v1/ids3/dikube", summary="DIKube 记录更新", deprecated=False)
def update_dikube(model: RequestDIKubeModel):
    dikube.update_dikube(model.id, DIKube(**model.dict()))
    return NormalResponse(msg="更新成功", data=None)


@router.delete("/api/v1/ids3/dikube", summary="DIKube 记录删除", deprecated=False)
def delete_dikube(dikube_id: str):
    try:
        dikube.delete_dikube(dikube_id)
        return NormalResponse(msg="删除成功", data=None)
    except Exception as e:
        return NormalResponse(code=500, msg="删除失败", data=str(e))


@router.get("/api/v1/ids3/dikube/detail", summary="DIKube 记录详情查询", deprecated=False)
def get_dikube_detail(dikube_id: str = Query(title='DIKube记录ID', description="DIKube记录ID")):
    try:
        result = dikube.get_dikube_detail(dikube_id)
        return NormalResponse(msg="查询详情成功", data=result)
    except Exception as e:
        return NormalResponse(code=500, msg="查询详情失败", data=str(e))


@router.get("/api/v1/ids3/dikube/sub", summary="DIKube 子节点查询", deprecated=False)
def get_sub_node(dikube_id: str = Query(title='DIKube记录ID', description="DIKube记录ID")):
    try:
        result = dikube.get_sub_nodes(dikube_id)
        return NormalResponse(msg="查询详情成功", data=result)
    except Exception as e:
        return NormalResponse(code=500, msg="查询详情失败", data=str(e))
