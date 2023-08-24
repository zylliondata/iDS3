# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 10:04 2023/7/20
# @Description: datahub graphql 接口封装
# @Version: Python 3.8.11
# @Modified By:

from src.config import ioDS3_config
from src.meta.utils import emitter_gms


class MetaManagement:
    # 类变量，它的值将在这个类的所有实例之间共享
    url = ioDS3_config.get("datahub").get('server') + ioDS3_config.get("datahub").get('route')
    token = ioDS3_config.get("datahub").get('token')

    def __init__(self):
        pass

    # datahub 元数据摄取
    def ingest_source(self, name, data_type, description, recipe, executor_id):
        query = """{ \"query\": \"mutation { createIngestionSource(input: { name: \\\"%s\\\" type: \\\"%s\\\" description: \\\"%s\\\" config: {recipe: \\\"%s\\\" executorId: \\\"%s\\\"}})}\"}""" \
                % (name, data_type, description, recipe, executor_id)
        print(query)
        result = emitter_gms(MetaManagement.url, query, MetaManagement.token)
        return result

    # datahub entity query
    def query_execution_request(self, data):
        # payload = EXECUTION_REQUEST_BEGIN + data + EXECUTION_REQUEST_END
        query = """{\"query\":\"{ executionRequest(urn:\\\"%s\\\") {urn result { status startTimeMs  durationMs  structuredReport{type serializedValue } }}}\",\"variables\":{}}""" \
                % data
        result = emitter_gms(MetaManagement.url, query, MetaManagement.token)
        return result

    def list_sources(self, start, count):
        query = """{\"query\":\"{listIngestionSources (input: {start:%s count:%s query: \\\"\\\"}){start count total ingestionSources {urn type  name  config { recipe } executions { start  count total   executionRequests {  urn  result { status   startTimeMs }}} }}}\",\"variables\":{}}""" % (
            start, count)
        result = emitter_gms(MetaManagement.url, query, MetaManagement.token)
        return result

    def list_sources_total(self, start, count):
        query = """{\"query\":\"{listIngestionSources (input: {start:%s count:%s}){total}}\",\"variables\":{}}""" % (
            start, count)
        result = emitter_gms(MetaManagement.url, query, MetaManagement.token)
        return result

    def detail_source(self, urn):
        query = """{\"query\":\"{ingestionSource(urn: \\\"%s\\\") {urn type config { recipe } executions { start count total  executionRequests { urn } } }}\",\"variables\":{}}""" % (
            urn)
        result = emitter_gms(MetaManagement.url, query, MetaManagement.token)
        return result

    def trigger_ingestion(self, urn):
        query = """{\"query\":\"mutation { createIngestionExecutionRequest(input: {ingestionSourceUrn: \\\"%s\\\"})}\"}""" % (
            urn)
        result = emitter_gms(MetaManagement.url, query, MetaManagement.token)
        return result

    def cancel_ingestion(self, ingestion_source_urn, execution_request_urn):
        query = """{\"query\":\"mutation{cancelIngestionExecutionRequest(input: {ingestionSourceUrn: \\\"%s\\\" executionRequestUrn: \\\"%s\\\"})}\",\"variables\":{}}""" % (
            ingestion_source_urn, execution_request_urn)
        result = emitter_gms(MetaManagement.url, query, MetaManagement.token)
        return result

    def aggr_platform(self):
        query = """{\"query\":\"{aggregateAcrossEntities(input: {facets: [\\\"platform\\\"]  orFilters:[] query: \\\"*\\\"  searchFlags:{}}) { facets { field displayName aggregations { value count }}}}\",\"variables\":{}}"""
        result = emitter_gms(MetaManagement.url, query, MetaManagement.token)
        return result

    def aggr_type(self):
        query = """{\"query\":\"{aggregateAcrossEntities(input: {facets: [ \\\"_entityType␞typeNames\\\", \\\"_entityType\\\" ]  orFilters:[] query: \\\"*\\\"  searchFlags:{}}) {facets {field displayName  aggregations { value count } }}}\",\"variables\":{}}"""
        result = emitter_gms(MetaManagement.url, query, MetaManagement.token)
        return result

    def query_entity(self, entity_type: str, keyword: str, start: int, count: int):
        query = """{\"query\":\"{search(input: { type: %s, query: \\\"%s\\\", start: %s, count: %s }) { start count total searchResults {entity {urn type ...on Dataset {name lastIngested}}}}}\",\"variables\":{}}""" % (
            entity_type, keyword, start, count)
        result = emitter_gms(MetaManagement.url, query, MetaManagement.token)
        return result
