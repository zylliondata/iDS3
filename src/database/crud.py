# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 15:15 2023/8/2
# @Description: 数据操作
# @Version: Python 3.8.11
# @Modified By:
import pymysql
import sqlalchemy.sql.functions
from sqlalchemy import select

from src.database.models import FileInfo, DIKubeQuery, DataSource, QueryHistory


class MySQLHelper:

    def __init__(self):
        pass

    def add(self, session, obj):
        """
        新增一个对象
        :param session: mysql session
        :param obj: Object
        :return:
        """
        try:
            session.add(obj)
            session.commit()
            session.refresh(obj)
        except pymysql.err.DataError as e:
            # Log or handle the specific data error
            print("Data error:", str(e))
            # Rollback the transaction
            session.rollback()

    def add_batch(self, session, objs):
        """
        批量新增
        :param session:
        :param objs: Object list
        :return:
        """
        session.add_all(objs)
        session.commit()
        session.refresh(objs)

    def delete(self, session, obj):
        """
        删除对象
        :param session:
        :param obj:
        :return:
        """
        session.delete(obj)
        session.commit()

    def update(self, session, obj):
        """
        更新对象
        :param session:
        :param obj:
        :return:
        """
        session.merge(obj)
        session.commit()
        session.refresh(obj)

    def count(self, session, obj):
        """
        根据对象ID，进行计数
        :param session:
        :param obj:
        :return:
        """
        total_count = session.execute(select(sqlalchemy.func.count(obj.id))).scalar_one()
        return total_count

    def query_page(self, session, obj, page_number: int, page_size: int):
        # 每页的记录数量
        limit = page_size
        # 计算起始偏移量
        offset = (page_number - 1) * page_size
        # sqlalchemy.sql.functions.count()
        stmt = select(obj).offset(offset).limit(limit)
        return session.execute(stmt).scalars().fetchall()

    def delete_by_id(self, session, obj, obj_id):
        stmt = select(obj).filter_by(id=obj_id)
        return session.delete(stmt)

    def query_by_id(self, session, obj, obj_id):
        stmt = select(obj).filter_by(id=obj_id)
        return session.execute(stmt).scalars().first()

    def query_by_source_urn(self, session, source_urn):
        """
        DataSource,根据sourceUrn查询对应的数据源信息
        :param session: 数据库会话
        :param source_urn:
        :return: object
        """
        stmt = select(DataSource).filter_by(sourceUrn=source_urn)
        return session.execute(stmt).scalars().first()

    def query_all_source_urn(self, session):
        """
        DataSource,查询所有sourceUrn
        :return: lists
        """
        stmt = select(DataSource.sourceUrn)
        rows = session.execute(stmt).scalars().fetchall()
        return rows

    def delete_by_source_urn(self, session, source_urn):
        stmt = select(DataSource).filter_by(sourceUrn=source_urn)
        session.delete(stmt)
        return True

    def query_trino_by_delta(self, session, delta_path):
        """
        根据delta 路径 查询trino表
        :param delta_path: delta/delta_table
        :return: str delta.deltalake.delta_table
        """
        stmt = select(FileInfo.trinoPath).filter_by(savePath=delta_path)
        query_result = session.execute(stmt)
        return query_result.scalars().first()

    def query_by_query_dikube_id(self, session, dikube_id):
        stmt = select(DIKubeQuery).filter_by(dikubeId=dikube_id)
        return session.execute(stmt).scalars().fetchall()

    def search_query_by_id(self, session, obj, query_id):
        stmt = select(obj).filter_by(queryId=query_id)
        return session.execute(stmt).scalars().fetchall()

    def query_history_by_query_id(self, session, query_id):
        stmt = select(QueryHistory).filter_by(queryId=query_id).order_by(
            QueryHistory.recordedAt.desc()).limit(10)
        return session.execute(stmt).scalars().fetchall()

    def delete_by_double_id(self, session, dikube_id, query_id):
        stmt = select(DIKubeQuery).filter_by(dikubeId=dikube_id, queryId=query_id)
        return session.delete(stmt)


    def query_by_sql(self, session, obj, sql_record):
        stmt = select(obj).filter_by(sqlRecord=sql_record)
        return session.execute(stmt).scalars().first()

    def query_by_catalog(self, session, obj, catalog):
        stmt = select(obj).filter_by(catalog=catalog)
        return session.execute(stmt).scalars().fetchall()

    def count_dikube(self, session, obj, project):
        """
        根据对象ID,经过project 过滤,进行计数
        :param session:
        :param obj:
        :param project:
        :return:
        """

        total_count = session.execute(select(sqlalchemy.func.count(obj.id)).filter_by(project=project)).scalar_one()
        return total_count

    def query_page_dikube(self, session, obj, project: str, page_number: int, page_size: int):
        # 每页的记录数量
        limit = page_size
        # 计算起始偏移量
        offset = (page_number - 1) * page_size
        # sqlalchemy.sql.functions.count()
        stmt = select(obj).filter_by(project=project).offset(offset).limit(limit)
        return session.execute(stmt).scalars().fetchall()

    def query_by_dikube_id(self, session, obj, dikube_id):
        stmt = select(obj).filter_by(dikubeId=dikube_id)
        return session.execute(stmt).scalars().fetchall()

    def query_dikube_by_name(self, session, obj, dikube_name):
        stmt = select(obj).filter_by(name=dikube_name)
        return session.execute(stmt).scalars().first()
