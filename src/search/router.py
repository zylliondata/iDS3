# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 17:19 2023/8/9
# @Description: 搜索服务路由
# @Version: Python 3.8.11
# @Modified By:
from fastapi import APIRouter, Query

from src.models import NormalResponse
from src.search.models import QueryRequestModel, QueryCreateModel, SearchQueryModel, QueryIDRequestModel
from src.search.service import SearchService

router = APIRouter()
search = SearchService()


@router.get("/api/v1/ids3/search/table", summary="根据datasetUrn查询表名称", deprecated=False)
def get_trino_table(urn: str = Query(title="数据源urn")):
    """
    根据datasetUrn查询表名称
    :param urn: datahub dataset urn
    :return: 表名称
    """
    try:
        result_path = search.get_table(urn)
        return NormalResponse(msg="查询成功", data=result_path)
    except Exception as e:
        return NormalResponse(code=500, msg="查询错误", data=str(e))


@router.get("/api/v1/ids3/search/preview", summary="根据datasetUrn预览对应的数据表内容", deprecated=False)
async def preview_table(urn: str = Query(title="数据源urn")):
    """
    根据datasetUrn预览数据
    :param urn: datahub dataset urn
    :return: 表数据，随机最多50条
    """
    try:
        result = search.preview_table(urn)
        return NormalResponse(msg="查询成功", data=result)
    except Exception as e:
        return NormalResponse(code=500, msg="查询错误", data=e)


@router.post("/api/v1/ids3/search/query", summary="根据SQL查询数据", deprecated=False,
             description="SELECT(全大写) * FROM(全大写)以及进行尝试时，强烈建议限制返回数据的数量！！！")
async def query_data(model: QueryRequestModel):
    try:
        result = search.get_data_by_query(model.data_source, model.search_query)
        count = search.count_data_by_query(model.data_source, model.search_query)
        return NormalResponse(msg="查询成功", data={"result": result, "count": count})
    except Exception as e:
        return NormalResponse(code=500, msg="查询错误", data=e)


@router.post("/api/v1/ids3/query", summary="SQL 记录创建", deprecated=False)
async def create_query(model: QueryCreateModel):
    try:
        result = search.create_query(model.datasetUrn, model.data_source, model.sqlRecord, model.description)
        return NormalResponse(msg="创建成功", data=result)
    except Exception as e:
        return NormalResponse(code=500, msg="创建失败", data=str(e))


@router.put("/api/v1/ids3/query", summary="SQL 记录更新", deprecated=False)
def update_query(model: SearchQueryModel):
    try:
        result = search.update_query(model)
        return NormalResponse(msg="更新成功", data=result)
    except Exception as e:
        return NormalResponse(code=500, msg="更新失败", data=str(e))


@router.get("/api/v1/ids3/query", summary="SQL 记录分页查询", deprecated=False)
def list_query(page_number: int = Query(title="当前页", default=1, ge=1, description="当前页码"),
               page_size: int = Query(title="分页大小", default=10, ge=1, le=1000, description="分页大小范围1-1000")):
    try:
        result = search.query_query_by_page(page_number, page_size)
        return NormalResponse(msg="查询成功", data=result)
    except Exception as e:
        return NormalResponse(code=500, msg="查询失败", data=str(e))


@router.delete("/api/v1/ids3/query", summary="SQL 记录删除", deprecated=False)
def delete_query(query_id: str):
    try:
        result = search.delete_query_query(query_id)
        return NormalResponse(msg="删除成功", data=result)
    except Exception as e:
        return NormalResponse(code=500, msg="删除失败", data=str(e))


@router.get("/api/v1/ids3/query/detail", summary="SQL 记录详情查询", deprecated=False)
def query_data_by_id(query_id: str = Query(title='SQL记录ID', description="SQL记录ID")):
    try:
        result = search.query_by_id(query_id)
        return NormalResponse(msg="查询详情成功", data=result)
    except Exception as e:
        return NormalResponse(code=500, msg="查询详情失败", data=str(e))


@router.post("/api/v1/ids3/query/dikube", summary="Query&DIKube 关联创建", deprecated=False)
def create_query_dikube_record(model: QueryIDRequestModel):
    search.add_query_dikube(model.queryId, model.catalogId)
    return NormalResponse(msg="创建成功", data=None)


@router.get("/api/v1/ids3/query/dikube/query", summary="根据queryID，获取关联的DIKube", deprecated=False)
def list_query_dikube(
        query_id: str = Query(title='SQL记录ID', description="SQL记录ID")
):
    result = search.list_query_dikube(query_id)
    return NormalResponse(msg="查询成功", data=result)


@router.get("/api/v1/ids3/query/dikube/dikube", summary="根据dikubeID，获取关联的query", deprecated=False)
def list_query_dikube(
        dikube_id: str = Query(title='DIKube记录ID', description="DIKube记录ID")
):
    result = search.list_dikube_query(dikube_id)
    return NormalResponse(msg="查询成功", data=result)


@router.get("/api/v1/ids3/query/dikube/page", summary="Query&DIKube 关联分页查询", deprecated=False)
def list_query_and_dikube(page_number: int = Query(title="当前页", default=1, ge=1, description="当前页码"),
                          page_size: int = Query(title="分页大小", default=10, ge=1, le=1000,
                                                 description="分页大小范围1-1000")):
    result = search.list_dikube_query_by_page(page_number, page_size)
    return NormalResponse(msg="查询成功", data=result)


@router.delete("/api/v1/ids3/query/dikube", summary="Query&DIKube 关联删除", deprecated=False)
def delete_query_dikube(model: QueryIDRequestModel):
    search.delete_query_dikube(model.queryId, model.catalogId)
    return NormalResponse(msg="删除成功", data=None)


@router.get("/api/v1/ids3/query/sync", summary="根据数据统计内容（实时更新）", deprecated=False)
async def sync_query_data():
    try:
        # 默认写死 catalog="delta-lake"， 该版本只进行delta-lake的实时数据统计
        data = search.get_growth_data_from_delta(catalog="delta-lake")
        return NormalResponse(msg="成功，更新记录：" + str(data), data=None)
    except Exception as e:
        return NormalResponse(code=500, msg="更新失败", data=e)


@router.get("/api/v1/ids3/query/history", summary="根据queryID，获取最近10条历史记录", deprecated=False)
def list_history_query(query_id: str = Query(title='SQL记录ID', description="SQL记录ID")):
    try:
        result = search.list_query_history(query_id)
        return NormalResponse(msg="查询成功", data=result)
    except Exception as e:
        return NormalResponse(code=500, msg="查询失败", data=str(e))