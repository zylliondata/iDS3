# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 17:46 2023/8/4
# @Description: datahub 元数据操作
# @Version: Python 3.8.11
# @Modified By:
import json
from contextlib import contextmanager

from src.database.database import SessionLocal
from src.database.models import DataSource
from src.database.crud import MySQLHelper
from src.meta.models import IngestSourceModel, SourceTotalModel, SearchDataModel, EntityType
from src.meta.repo import MetaManagement
from src.meta.utils import get_enum_value


class MetaService:

    def __init__(self):
        self.helper = MySQLHelper()
        meta = MetaManagement()
        self.meta = meta

    @contextmanager
    def db_session(self):
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def ingest_source(self, name: str, data_type: str, description: str, recipe: str, executor_id: str) -> str:
        # 创建数据源摄取任务
        ingest_source_result = self.meta.ingest_source(name=name, data_type=data_type,
                                                       description=description,
                                                       recipe=recipe,
                                                       executor_id=executor_id)
        # 获取数据源摄取任务的 ingestionSourceUrn; 获取source urn
        datahub_ingestion_source_urn = ingest_source_result.get('data').get('createIngestionSource')
        # 获取数据源摄取任务的详细信息
        detail_source_result = self.meta.detail_source(datahub_ingestion_source_urn)
        # 触发摄取任务
        trigger_ingestion_result = self.meta.trigger_ingestion(datahub_ingestion_source_urn)
        # 获取摄取任务的 executionRequestUrn
        execution_request_urn = trigger_ingestion_result.get('data').get('createIngestionExecutionRequest')
        # 根据 executionRequestUrn 获取摄取任务的执行状态
        query_execution_request_urn = self.meta.query_execution_request(execution_request_urn)
        # 获取任务执行的情况
        return query_execution_request_urn

    def get_container_urn(self, query_execution_request_urn):
        report = query_execution_request_urn.get('data').get('executionRequest').get('result').get(
            'structuredReport').get('serializedValue')
        report_json = json.loads(report)
        # 获取任务执行结果中的 container_urn
        container_urn = report_json.get('source').get('report').get('entities').get('container')
        return container_urn

    @staticmethod
    def get_source_recipe(source_type, recipe):
        recipe = json.loads(recipe)
        result_dict = {}
        if source_type == "mysql":
            result_dict = {
                "host": recipe.get('source').get('config').get('host_port'),
                "username": recipe.get('source').get('config').get('username'),
                "password": recipe.get('source').get('config').get('password')
            }
        elif source_type == "mongodb":
            try:
                username = recipe.get('source').get('config').get('username')
            except Exception as e:
                username = ""
            try:
                password = recipe.get('source').get('config').get('password')
            except Exception as e:
                password = ""
            result_dict = {
                "connect_uri": recipe.get('source').get('config').get('connect_uri'),
                "username": username,
                "password": password
            }
        elif source_type == "delta-lake":
            try:
                aws_region = recipe.get('source').get('config').get('s3').get('aws_config').get('aws_region')
            except Exception as e:
                aws_region = ""
            result_dict = {
                "base_path": recipe.get('source').get('config').get('base_path'),
                "aws_region": aws_region,
                "aws_endpoint_url": recipe.get('source').get('config').get('s3').get('aws_config').get(
                    'aws_endpoint_url'),
                "aws_access_key_id": recipe.get('source').get('config').get('s3').get('aws_config').get(
                    'aws_access_key_id'),
                "aws_secret_access_key": recipe.get('source').get('config').get('s3').get('aws_config').get(
                    'aws_secret_access_key'),
            }
        else:
            pass
        return json.dumps(result_dict)

    def get_source_page(self, start, count):
        total = self.meta.list_sources_total(start, count)
        print(total)
        model = SourceTotalModel(**total)
        return model.data.listIngestionSources.total

    def list_sources(self, start=0, count=10):
        # 获取分页数据
        total_sources = self.get_source_page(start, count)
        # 计算总页数
        total_pages = (total_sources // count) + 1
        # 开始分页
        deleted_source = []
        with self.db_session() as session:
            source_urns_list = self.helper.query_all_source_urn(session)
        for page in range(1, total_pages + 1):
            current_start = (page - 1) * count
            source_result = self.meta.list_sources(current_start, count)
            model = IngestSourceModel(**source_result)
            start = model.data.listIngestionSources.start
            count = model.data.listIngestionSources.count
            total = model.data.listIngestionSources.total
            ingestion_sources = model.data.listIngestionSources.ingestionSources

            for ingestion_source in ingestion_sources:
                # print(ingestion_source)
                result_model = DataSource()
                result_model.sourceUrn = ingestion_source.urn
                result_model.sourceType = ingestion_source.type
                result_model.sourceName = ingestion_source.name
                recipe = ingestion_source.config.get('recipe')
                if ingestion_source.urn not in source_urns_list:
                    deleted_source.append(ingestion_source.urn)

                execution_requests = ingestion_source.executions.executionRequests

                for execution_request in execution_requests:
                    execution_result_status = execution_request.result.status
                    if execution_result_status == "SUCCESS":
                        recipe = self.get_source_recipe(ingestion_source.type, recipe)
                        result_model.sourceRecipe = recipe
                        result_model.executionResultStatus = execution_result_status
                        result_model.executionRequestUrn = execution_request.urn
                        result_model.executionResultStatus = execution_result_status
                        result_model.executionResultStartTimeMs = execution_request.result.startTimeMs
                        # 判断记录是否存在，不存在直接插入，存在则更新

                        with self.db_session() as session:
                            query_result = self.helper.query_by_source_urn(session, ingestion_source.urn)

                        if query_result:
                            # 对象操作
                            if query_result.executionResultStartTimeMs < \
                                    execution_request.result.startTimeMs:
                                result_model.id = query_result.id
                                with self.db_session() as session:
                                    self.helper.update(session, result_model)
                            else:
                                continue
                        else:
                            # print("新增")
                            with self.db_session() as session:
                                self.helper.add(session, result_model)
                        break
        # 如记录中存在，但datahub source 中不存在，则删除对应的数据源
        if deleted_source:
            for urn in deleted_source:
                with self.db_session() as session:
                    self.helper.delete_by_source_urn(session, urn)
        return "SUCCESS"

    def list_entities(self, entity_type, keyword, start, count):
        entity_value = get_enum_value(EntityType, entity_type)
        if entity_value is None:
            raise KeyError("entity_type is not in EntityType")
        data_dict = self.meta.query_entity(entity_value, keyword, start, count)
        data = data_dict.get('data').get('search')
        model = {
            "start": data.get('start'),
            "count": data.get('count'),
            "total": data.get('total'),
        }
        search_results = data.get('searchResults')
        entity_list = []
        for search_result in search_results:
            # print(search_result.entity)
            inner_model = {
                "urn": search_result.get('entity').get('urn'),
                "entity_type": search_result.get('entity').get('type'),
                "name": search_result.get('entity').get('name'),
                "last_ingested": search_result.get('entity').get('lastIngested')
            }
            entity_list.append(inner_model)
        model['searchResults'] = entity_list
        return SearchDataModel(**model)
