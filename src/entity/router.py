# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 10:51 2023/7/25
# @Description: datahub sdk 封装
# @Version: Python 3.8.11
# @Modified By:

from fastapi import APIRouter, Query
from src.config import ioDS3_config

from src.entity.models import LineageStreams
from src.entity.service import EntityManagement
from src.models import NormalResponse

router = APIRouter()

server = ioDS3_config.get("datahub").get("server")
token = ioDS3_config.get("datahub").get("token")

entity = EntityManagement(server=server, token=token)


@router.get("/api/v1/ids3/entity/detail", summary="元数据详情")
def detail_dataset(urn: str = Query(title="数据源urn")):
    result = entity.detail_dataset(urn)
    return NormalResponse(msg="元数据详情", data=result)


@router.delete("/api/v1/ids3/entity/delete", summary="根据dataset urn 删除元数据")
def delete_dataset(urn: str = Query(title="数据源urn")):
    entity.soft_delete_dataset(urn)
    return NormalResponse(msg="删除成功", data=None)


@router.get("/api/v1/ids3/entity/browse", summary="获取 Datahub 对应dataset 操作连接")
def browse_dataset(urn: str = Query(title="数据源urn")):
    result = entity.browse_ui(urn)
    return NormalResponse(msg="Datahub UI", data=result)


@router.post("/api/v1/ids3/entity/lineage", summary="创建数据沿袭")
def create_lineage(model: LineageStreams):
    if len(model.up_entity.field_path) > 0 and len(model.down_entity.field_path) > 0:
        result = entity.create_column_lineage(model.up_entity, model.down_entity)
        return NormalResponse(msg="列级别数据沿袭创建", data=result)
    else:
        result = entity.create_lineage(model.up_entity.dataset_urn, model.down_entity.dataset_urn)
        return NormalResponse(msg="表级别数据沿袭创建", data=result)
