# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 16:18 2023/7/21
# @Description: Todo
# @Version: Python 3.8.11
# @Modified By:
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class DataHubEntity(Enum):
    DOMAIN = 'DOMAIN'
    DATASET = 'dataset'
    CORP_USER = 'CORP_USER'
    CORP_GROUP = 'CORP_GROUP'
    DATA_PLATFORM = 'DATA_PLATFORM'
    DASHBOARD = 'DASHBOARD'
    NOTEBOOK = 'NOTEBOOK'
    CHART = 'CHART'
    DATA_FLOW = 'DATA_FLOW'
    DATA_JOB = 'DATA_JOB'
    TAG = 'TAG'
    GLOSSARY_TERM = 'GLOSSARY_TERM'
    GLOSSARY_NODE = 'GLOSSARY_NODE'
    CONTAINER = 'container'
    MLMODEL = 'MLMODEL'
    MLMODEL_GROUP = 'MLMODEL_GROUP'
    MLFEATURE_TABLE = 'MLFEATURE_TABLE'
    MLFEATURE = 'MLFEATURE'
    MLPRIMARY_KEY = 'MLPRIMARY_KEY'
    INGESTION_SOURCE = 'INGESTION_SOURCE'
    EXECUTION_REQUEST = 'EXECUTION_REQUEST'
    ASSERTION = 'ASSERTION'
    DATA_PROCESS_INSTANCE = 'DATA_PROCESS_INSTANCE'
    DATA_PLATFORM_INSTANCE = 'DATA_PLATFORM_INSTANCE'
    ACCESS_TOKEN = 'ACCESS_TOKEN'
    TEST = 'TEST'
    DATAHUB_POLICY = 'DATAHUB_POLICY'
    DATAHUB_ROLE = 'DATAHUB_ROLE'
    POST = 'POST'
    SCHEMA_FIELD = 'SCHEMA_FIELD'
    DATAHUB_VIEW = 'DATAHUB_VIEW'
    QUERY = 'QUERY'
    DATA_PRODUCT = 'DATA_PRODUCT'
    CUSTOM_OWNERSHIP_TYPE = 'CUSTOM_OWNERSHIP_TYPE'
    ROLE = 'ROLE'


class QueryEntities(BaseModel):
    entity_type: str = 'dataset'
    start: int = 0
    count: int = 10


class QueryDataset(BaseModel):
    entity_types: List[str] = ['dataset']
    platform: Optional[str] = None
    env: Optional[str] = None
    query: Optional[str] = None
    batch_size: int = 1000
    start: int = 0
    count: int = 10


class LineageEntity(BaseModel):
    dataset_urn: str
    field_path: List[str]


class LineageStreams(BaseModel):
    up_entity: LineageEntity
    down_entity: LineageEntity
