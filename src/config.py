# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 10:05 2023/7/20
# @Description: Nacos 配置中心
# @Version: Python 3.8.11
# @Modified By:
import json
import os

import nacos

nacos_client = nacos.NacosClient(
    server_addresses=os.environ.get('NACOS_SERVER', 'xxx:8848'),
    namespace=os.environ.get('NACOS_NAMESPACE', 'your namespace'),
    username=os.environ.get('NACOS_USERNAME', 'your username'),
    password=os.environ.get('NACOS_PASSWORD', 'your password')
)

nacos_ioDS3_config = nacos_client.get_config(data_id="ioDS3", group="DEFAULT_GROUP")
ioDS3_config = json.loads(nacos_ioDS3_config)
