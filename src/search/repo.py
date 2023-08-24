# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 17:38 2023/8/8
# @Description: Trino SDK 操作类
# @Version: Python 3.8.11
# @Modified By:
import json
from datetime import datetime

from src.search.utils import json_encoder as default


class SearchRepo:

    def __init__(self):
        pass

    # 在指定 table 中查询数据
    def show_tables(self, session, search_query):
        cur = session.cursor()
        try:
            cur.execute(search_query)
            rows = cur.fetchall()
            # 获取列名
            columns = [col[0] for col in cur.description]
            # 构造包含字段名和值的字典列表
            data = []
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    if isinstance(value, float):
                        row_dict[columns[i]] = str(value)
                    elif isinstance(value, datetime):
                        row_dict[columns[i]] = value
                    else:
                        row_dict[columns[i]] = value
                data.append(row_dict)

            # 将结果转换为JSON格式的字符串并返回
            return json.dumps(data, default=default)
        finally:
            cur.close()

    def show_table_sample(self, session, table_name):
        cur = session.cursor()
        try:
            cur.execute(f"SELECT * FROM {table_name} TABLESAMPLE limit 10")
            rows = cur.fetchall()
            # 获取列名
            columns = [col[0] for col in cur.description]
            # 构造包含字段名和值的字典列表
            data = []
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    if isinstance(value, float):
                        row_dict[columns[i]] = str(value)
                    elif isinstance(value, datetime):
                        row_dict[columns[i]] = value
                    else:
                        row_dict[columns[i]] = value
                data.append(row_dict)

            # 将结果转换为JSON格式的字符串并返回
            return json.dumps(data, default=default)
        finally:
            cur.close()

    def count_query(self, session, search_query):
        cur = session.cursor()
        try:
            cur.execute(search_query)
            return cur.fetchall()
        finally:
            cur.close()
