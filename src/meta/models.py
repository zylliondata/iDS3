# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 10:04 2023/7/20
# @Description: Todo
# @Version: Python 3.8.11
# @Modified By:
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class ResultModel(BaseModel):
    status: str
    startTimeMs: int


class ExecutionRequestModel(BaseModel):
    urn: str
    result: ResultModel


class InnerExecutionRequestModel(BaseModel):
    start: int
    count: int
    total: int
    executionRequests: List[ExecutionRequestModel]


class IngestionSourceModel(BaseModel):
    urn: str
    type: str
    name: str
    config: dict
    executions: InnerExecutionRequestModel


class ListIngestionSourcesModel(BaseModel):
    start: int
    count: int
    total: int
    ingestionSources: List[IngestionSourceModel]


class DataModel(BaseModel):
    listIngestionSources: ListIngestionSourcesModel


class IngestSourceModel(BaseModel):
    data: DataModel
    extensions: dict


# 获取分页的model
class ListIngestionSourcesResponse(BaseModel):
    total: int


class Data(BaseModel):
    listIngestionSources: ListIngestionSourcesResponse


class SourceTotalModel(BaseModel):
    data: Data
    extensions: dict


class EntityType(Enum):
    DATASET = "DATASET"
    CONTAINER = "CONTAINER"


# query entity
class QueryEntities(BaseModel):
    entity_type: str = Field(default=EntityType.DATASET.value, description="实体类型")
    start: int = Field(default=0, gte=0, description="起始页不能为负数")
    count: int = Field(default=10, gt=0, description="分页大小必须大于零")
    keyword: Optional[str] = ""


class SearchResult(BaseModel):
    urn: str
    entity_type: str
    name: str
    last_ingested: int


class SearchDataModel(BaseModel):
    start: int
    count: int
    total: int
    searchResults: List[SearchResult]


class ExecutionRequestModel(BaseModel):
    urn: str = 'urn:li:entity:(urn:li:dataPlatform:mysql,mysql,PROD)'


class CancelExecutionRequestModel(BaseModel):
    ingestion_source_urn: str = "urn:li:dataHubIngestionSource:4c895926-6be6-4bf8-bbd6-a1d7f0850f86"
    execution_request_urn: Optional[str] = "urn:li:dataHubExecutionRequest:0299831d-4ae0-4174-be2a-676e5657069a"
