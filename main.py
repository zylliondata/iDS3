import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from tortoise.exceptions import DoesNotExist, IntegrityError, ValidationError, OperationalError

from src import exceptions
from src.dikube.router import router as dikube_router
from src.entity.router import router as entity_router
from src.meta.router import router as meta_router
from src.models import NormalResponse
from src.search.router import router as search_router

description = """

ioDS3 V1.5 接口文档. 🚀

## 目的

进行元数据的管理、统一的SQL查询、数据可视化等功能聚合

## 概念

* DataSpace
* DataMesh
* DataFarbic

## 术语

* Datahub
* Trino
* Superset
* Spark

"""

app = FastAPI(
    title="ioDS3 API",
    description=description,
    # summary="ioDS3 API",
    version="1.5.0",
    # terms_of_service="暂无",
    contact={
        "name": "王明浩",
        "email": "wangmh@zylliondata.com",
    },
    license_info={
        "name": "Zylliondata 2.0 License",
        "url": "https://www.zylliondata.com",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# 异常错误处理
app.add_exception_handler(HTTPException, exceptions.http_error_handler)
app.add_exception_handler(RequestValidationError, exceptions.http422_error_handler)
app.add_exception_handler(exceptions.UnicornException, exceptions.unicorn_exception_handler)
app.add_exception_handler(DoesNotExist, exceptions.mysql_does_not_exist)
app.add_exception_handler(IntegrityError, exceptions.mysql_integrity_error)
app.add_exception_handler(ValidationError, exceptions.mysql_validation_error)
app.add_exception_handler(OperationalError, exceptions.mysql_operational_error)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(meta_router, tags=["数据源管理"])
app.include_router(entity_router, tags=["元数据管理"])
app.include_router(dikube_router, tags=["DIKube管理"])
app.include_router(search_router, tags=["搜索管理"])
# app.include_router(graph_router, tags=["节点管理"])


@app.get("/api/v1/ids3/health", summary="健康检查", deprecated=False, tags=["健康检查"])
def health_check():
    """
    用于检测服务是否健康的API,应一直返回相同的状态
    :return: NormalResponse
    """
    result = "Healthy"
    return NormalResponse(msg="健康检查", data=result)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
