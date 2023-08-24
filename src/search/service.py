# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 17:43 2023/8/8
# @Description: 搜索查询服务
# @Version: Python 3.8.11
# @Modified By:

import uuid
from contextlib import contextmanager
from datetime import datetime
from trino.auth import BasicAuthentication
from trino.dbapi import connect

from src.config import ioDS3_config
from src.database.crud import MySQLHelper
from src.database.database import SessionLocal
from src.database.models import SearchQuery, DIKubeQuery, DIKube, QueryHistory
from src.search.models import SearchQueryModel
from src.search.repo import SearchRepo
from src.search.utils import urn_schema, select_count


class SearchService:

    def __init__(self):
        self.search_repo = SearchRepo()
        self.helper = MySQLHelper()

    @contextmanager
    def db_session(self):
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    @contextmanager
    def trino_session(self, catalog):
        trino_session = connect(
            host=ioDS3_config['trino']['host'],
            port=ioDS3_config['trino']['port'],
            user=ioDS3_config['trino']['user'],
            catalog=catalog,
            auth=BasicAuthentication(ioDS3_config['trino']['auth_user'], ioDS3_config['trino']['auth_pwd']),
            http_scheme=ioDS3_config['trino']['http_scheme'],
            verify=ioDS3_config['trino']['verify']
        )
        try:
            yield trino_session
        finally:
            trino_session.close()

    def get_trino_path(self, save_path):
        with self.db_session() as session:
            return self.helper.query_trino_by_delta(session, save_path)

    def get_table(self, data_set_urn):
        urn_dict = urn_schema(data_set_urn)
        if urn_dict:
            if urn_dict['catalog'] == 'delta-lake':
                return self.get_trino_path(urn_dict['table'])
            else:
                result = urn_dict['catalog'] + '.' + urn_dict['table']
                return result

    def preview_table(self, data_set_urn):
        table = self.get_table(data_set_urn)
        print(table)
        if table:
            catalog = table.split('.')[0]
            with self.trino_session(catalog) as trino_session:
                result_rows = self.search_repo.show_table_sample(trino_session, table)
            # print(result_rows)
            return result_rows
        else:
            return None

    def get_data_by_query(self, catalog, search_query: str):
        if "limit" not in search_query:
            search_query = search_query + " limit 51"
        with self.trino_session(catalog) as trino_session:
            return self.search_repo.show_tables(trino_session, search_query)

    def count_data_by_query(self, catalog: str, search_query: str) -> int:
        count_query = select_count(search_query)
        # print("----------------------------" + count_query)
        if count_query:
            with self.trino_session(catalog) as trino_session:
                return self.search_repo.count_query(trino_session, count_query)[0][0]
        else:
            return -1  # 查询语句不合法

    def create_query(self, data_set_urn: str, catalog: str, search_query: str, description: str):
        if catalog not in ['mysql', 'mongodb', 'delta-lake']:
            raise Exception("data source 参数错误!!!")
        if "urn" not in data_set_urn:
            raise Exception("datasetUrn 参数错误!!!")
        with self.db_session() as session:
            has_query = self.helper.query_by_sql(session, SearchQuery, search_query)
            if has_query:
                raise Exception("该query已经存在!!!")
            print("***********")
            total_nums = self.count_data_by_query(catalog, search_query)
            print(str(total_nums) + "***********")
            query_model = SearchQuery(id=str(uuid.uuid4()), sqlRecord=search_query, datasetUrn=data_set_urn,
                                      description=description,
                                      catalog=catalog,
                                      createdAt=datetime.utcnow(), cornJob=None, dailyGrowth=0,
                                      totalCount=total_nums, updatedAt=datetime.utcnow())
            self.helper.add(session, query_model)
        return query_model.id

    def update_query(self, query_model: SearchQueryModel):
        with self.db_session() as session:
            source_query = self.helper.query_by_id(session, SearchQuery, query_model.id)

            source_query.sqlRecord = query_model.sqlRecord
            source_query.description = query_model.description
            source_query.updatedAt = datetime.utcnow()
            total_nums = self.count_data_by_query(source_query.catalog, query_model.sqlRecord)
            source_query.totalCount = total_nums
            self.helper.update(session, source_query)

    def delete_query_query(self, query_id: str):
        with self.db_session() as session:
            model = self.helper.query_by_id(session, SearchQuery, query_id)
            if model:
                self.helper.delete(session, model)
                self.graph.delete_query(query_id)
            else:
                raise Exception("该 ID 不存在!!!")
        return query_id

    def query_by_id(self, query_id: str):
        with self.db_session() as session:
            return self.helper.query_by_id(session, SearchQuery, query_id)

    def query_query_by_page(self, page: int, size: int):
        with self.db_session() as session:
            total_count = self.helper.count(session, SearchQuery)
        with self.db_session() as session:
            query_data = self.helper.query_page(session, SearchQuery, page, size)
        return {"data": query_data, "count": total_count}

    def add_query_dikube(self, query_id: str, dikube_id: str):
        query_model = DIKubeQuery(queryId=query_id, dikubeId=dikube_id)
        with self.db_session() as session:
            self.helper.add(session, query_model)

    def delete_query_dikube(self, query_id: str, dikube_id: str):
        with self.db_session() as session:
            self.helper.delete_by_double_id(session, dikube_id, query_id)

    def list_query_dikube(self, query_id: str):
        with self.db_session() as session:
            return self.helper.search_query_by_id(session, DIKubeQuery, query_id)

    def list_dikube_query(self, dikube_id: str):
        with self.db_session() as session:
            return self.helper.query_by_query_dikube_id(session, dikube_id)

    def list_dikube_query_by_page(self, page: int, size: int):
        with self.db_session() as session:
            count = self.helper.count(session, DIKubeQuery)
        with self.db_session() as session:
            return {"data": self.helper.query_page(session, DIKubeQuery, page, size), "count": count}

    def add_dikube(self, description: str, status: bool, name: str):
        dikube_model = DIKube(id=uuid.uuid4(), description=description, status=status, name=name,
                              createdAt=datetime.utcnow())
        with self.db_session() as session:
            self.helper.add(session, dikube_model)

    def update_dikube(self, dikube_id: str, dikube_model: DIKube):
        with self.db_session() as session:
            source_dikube = self.helper.query_by_id(session, DIKube, dikube_id)
        source_dikube.description = dikube_model.description
        source_dikube.status = dikube_model.status
        source_dikube.name = dikube_model.name
        source_dikube.updatedAt = datetime.utcnow()
        with self.db_session() as session:
            self.helper.update(session, source_dikube)

    def delete_dikube(self, dikube_id: str):
        with self.db_session() as session:
            self.helper.delete_by_id(session, DIKube, dikube_id)

    def query_dikube_by_page(self, page: int, size: int):
        with self.db_session() as session:
            return self.helper.query_page(session, DIKube, page, size)

    def save_query_history(self, model: QueryHistory):
        with self.db_session() as session:
            self.helper.add(session, model)

    def get_growth_data_from_delta(self, catalog: str):
        count = 0
        with self.db_session() as session:
            source_query = self.helper.query_by_catalog(session, SearchQuery, catalog)
            for query_obj in source_query:
                # 用于计算增长量
                temp = query_obj.totalCount
                total_nums = self.count_data_by_query(catalog, query_obj.sqlRecord)
                query_obj.totalCount = total_nums
                query_obj.dailyGrowth = total_nums - temp
                query_obj.updatedAt = datetime.utcnow()
                self.helper.update(session, query_obj)
                self.helper.add(session,
                                QueryHistory(
                                    queryId=query_obj.id,
                                    catalog=query_obj.catalog,
                                    sqlRecord=query_obj.sqlRecord,
                                    totalCount=query_obj.totalCount,
                                    dailyGrowth=query_obj.dailyGrowth,
                                    createdAt=query_obj.updatedAt,
                                    recordedAt=query_obj.updatedAt
                                )
                                )
                count += 1
        return count

    def list_query_history(self, query_id: str):
        with self.db_session() as session:
            return self.helper.query_history_by_query_id(session, query_id)
