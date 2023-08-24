# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 17:37 2023/8/9
# @Description: 搜索请求模型
# @Version: Python 3.8.11
# @Modified By:
from typing import Optional

from pydantic import BaseModel, Field


class QueryRequestModel(BaseModel):
    data_source: str = Field(description="Demo 数据源: mysql、mongodb、delta-lake 三种")
    search_query: str = Field(description="查询语句, SELECT * FROM table_name WHERE xxx limit 10")


class QueryModel(BaseModel):
    id: str = Field(description="查询id")
    data_source: str = Field(description="Demo数据源: mysql、mongodb、delta-lake 三种")
    description: Optional[str] = Field(description="查询描述")
    sqlRecord: str = Field(description="查询语句, SELECT * FROM table_name WHERE xxx limit 10")
    datasetUrn: str = Field(description="数据源urn")


class QueryCreateModel(BaseModel):
    data_source: str = Field(default="mysql", description="Demo数据源: mysql、mongodb、delta-lake 三种")
    sqlRecord: str = Field(description="查询语句, SELECT * FROM table_name WHERE xxx limit 10")
    datasetUrn: str = Field(description="数据源urn")
    description: Optional[str] = Field(description="查询描述")


class QueryIDRequestModel(BaseModel):
    queryId: str = Field(description="SQL 的 ID")
    catalogId: str = Field(default=None, description="catalog or dikube ID")


class SearchQueryModel(BaseModel):
    id: str
    sqlRecord: Optional[str] = Field(description="查询语句, SELECT * FROM table_name WHERE xxx limit 10")
    description: Optional[str] = Field(description="查询描述")


    class Config:
        orm_mode = True
