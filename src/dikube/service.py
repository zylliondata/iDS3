# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 14:28 2023/8/9
# @Description: DIKube 服务类
# @Version: Python 3.8.11
# @Modified By:
from contextlib import contextmanager
from datetime import datetime

from src.database.crud import MySQLHelper
from src.database.database import SessionLocal
from src.database.models import DIKube


class DIKubeService:
    def __init__(self):
        self.helper = MySQLHelper()

    @contextmanager
    def db_session(self):
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def create_dikube(self, model: DIKube):
        if model.project not in ["catalog", "dikube"]:
            raise Exception("project 参数错误,[catalog|dikube]")
        if model.dikubeId is None:
            model.dikubeId = "root"
        with self.db_session() as session:
            dikube = self.helper.query_dikube_by_name(session, DIKube, model.name)
            if dikube:
                raise Exception("项目名称已存在")
            self.helper.add(session, model)

    def get_dikube_detail(self, dikube_id: str):
        with self.db_session() as session:
            dikube = self.helper.query_by_id(session, DIKube, dikube_id)
            return dikube

    def get_sub_nodes(self, dikube_id: str):
        with self.db_session() as session:
            dikube = self.helper.query_by_id(session, DIKube, dikube_id)
            if dikube is None:
                raise Exception("未找到对应的记录")
            sub_nodes = self.helper.query_by_dikube_id(session, DIKube, dikube_id)
            return sub_nodes

    def query_dikube_by_page(self, project: str, page_number: int, page_size: int):
        with self.db_session() as session:
            total_nums = self.helper.count_dikube(session, DIKube, project)
            search_result = self.helper.query_page_dikube(session, DIKube, project=project,
                                                          page_number=page_number, page_size=page_size)

        return {"total_nums": total_nums, "search_result": search_result}

    def delete_dikube(self, dikube_id: str):
        with self.db_session() as session:
            # 删除与Query 之间的关联关系
            models = self.helper.query_by_query_dikube_id(session, dikube_id)
            if models:
                for model in models:
                    self.helper.delete(session, model)
            dikube = self.helper.query_by_id(session, DIKube, dikube_id)
            if dikube:
                self.helper.delete(session, dikube)
                # 删除子节点,
                sub_dikubes = self.helper.query_by_dikube_id(session, DIKube, dikube_id)
                for sub_dikube in sub_dikubes:
                    self.delete_dikube(sub_dikube.id)
            else:
                raise Exception("未找到对应的记录")

    def update_dikube(self, dikube_id: str, dikube: DIKube):
        if dikube.dikubeId is None:
            dikube.dikubeId = "root"
        with self.db_session() as session:
            exits_dikube = self.helper.query_by_id(session, DIKube, dikube.dikubeId)
            if exits_dikube is None and dikube.dikubeId != "root":
                raise Exception("未找到对应的记录")

            source_dikube = self.helper.query_by_id(session, DIKube, dikube_id)
            print(source_dikube)
            source_dikube.name = dikube.name
            source_dikube.description = dikube.description
            source_dikube.status = dikube.status
            source_dikube.userID = None
            source_dikube.updatedAt = datetime.utcnow()
            self.helper.update(session, source_dikube)