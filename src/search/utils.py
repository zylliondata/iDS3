# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 17:57 2023/8/8
# @Description: Todo
# @Version: Python 3.8.11
# @Modified By:
import json
import re
from datetime import datetime


def urn_schema(dataset_urn):
    """
    根据 dataset urn 解析 schema
    :param dataset_urn:
    :return:
    """
    pattern = r'urn:li:dataPlatform:(.*?),(.*?),'
    matches = re.findall(pattern, dataset_urn)
    print(matches)
    if matches:
        catalog = matches[0][0]
        if catalog == 'delta-lake':
            table = matches[0][1]
            schema = table.split('/')
            return {"catalog": catalog, "table": schema[0] + '/' + schema[1]}
        table = matches[0][1]
        schema = table.split('.')
        return {"catalog": catalog, "table": '\"' + schema[0] + '\".\"' + schema[1] + '\"'}
    else:
        return None


def select_count(search_query: str):
    pattern = r"SELECT (.*) FROM"
    m = re.search(pattern, search_query)
    print(search_query, m)
    if m:
        between_select_from = m.group(1)
        new_query = search_query.replace(between_select_from, "COUNT(" + between_select_from + ") as total_count")
        return new_query
    else:
        return None


def json_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
