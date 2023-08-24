# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 10:04 2023/7/20
# @Description: 工具类
# @Version: Python 3.8.11
# @Modified By:
import json

import requests


def emitter_gms(url, data, token=None):
    '''
    发送 graphql 请求
    :param url: datahub url
    :param data: graphql data
    :param token: openapi token
    :return:
    '''
    authorization = 'Bearer ' + token
    if token is None:
        headers = {'Content-Type': 'application/json'}
    else:
        headers = {'Authorization': authorization, 'Content-Type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    print(response.status_code)
    return json.loads(response.text)


def get_enum_value(enum_class, member_name):
    try:
        member = enum_class[member_name]
        return member.value
    except KeyError:
        return None
