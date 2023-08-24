# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 11:24 2023/8/8
# @Description: 单元测试
# @Version: Python 3.8.11
# @Modified By:

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_healthy():
    response = client.get("/api/v1/ids3/health")
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "msg": "active",
        "result": "Healthy"
    }
