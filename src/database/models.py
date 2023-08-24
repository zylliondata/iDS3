# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 13:53 2023/8/4
# @Description: 数据库ORM模型
# @Version: Python 3.8.11
# @Modified By:

from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Integer, BigInteger, func, DateTime

from src.database.database import Base


class DataSource(Base):
    __tablename__: str = 'data_source'

    id = Column(Integer, primary_key=True, comment='数据源唯一标识')
    sourceUrn = Column(String(100), unique=True, nullable=False, comment='数据源Urn')
    sourceType = Column(String(20), comment='数据源类型')
    sourceName = Column(String(50), comment='数据源名称')
    sourceRecipe = Column(Text, comment='数据源配置')
    executionRequestUrn = Column(String(100), comment='数据源执行请求Urn')
    executionResultStatus = Column(String(10), comment='数据源执行结果状态')
    executionResultStartTimeMs = Column(BigInteger, comment='数据源执行结果开始时间')

    createdAt = Column(DateTime, server_default=func.now(), comment='创建时间')
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')


    def __repr__(self) -> str:
        return f"Datasource(id={self.id}, " \
               f"sourceUrn={self.sourceUrn}, " \
               f"sourceType={self.sourceType}, " \
               f"sourceName={self.sourceName}, createdAt={self.createdAt}, updatedAt={self.updatedAt}" \
               f"sourceRecipe={self.sourceRecipe}, " \
               f"executionRequestUrn={self.executionRequestUrn}," \
               f"executionResultStatus={self.executionResultStatus}, " \
               f"executionResultStartTimeMs={self.executionResultStartTimeMs})"


class FileInfo(Base):
    __tablename__ = 'file_info'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增整数类型id')
    savePath = Column(String(255), comment='文件MINIO保存路径')
    trinoPath = Column(String(255), comment='TRINO保存路径')
    description = Column(Text, comment='文件描述')

    createdAt = Column(DateTime, server_default=func.now(), comment='创建时间')
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def __repr__(self) -> str:
        return f"FileInfo(id={self.id}, savePath={self.savePath}, trinoPath={self.trinoPath}, " \
               f"createdAt={self.createdAt}, description={self.description})"


class DIKube(Base):
    __tablename__ = 'dikube'

    id = Column(String(50), primary_key=True)
    description = Column(String(255))
    userID = Column(String(255))
    status = Column(Boolean)
    project = Column(String(20))
    name = Column(String(20))
    dikubeId = Column(String(50))
    createdAt = Column(DateTime, server_default=func.now(), comment='创建时间')
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def __repr__(self):
        return f"DIKube(id={self.id}, description={self.description}, userID={self.userID}, " \
               f"status={self.status}, project={self.project},name={self.name}, dikubeId={self.dikubeId}," \
               f"createdAt={self.createdAt}, updatedAt={self.updatedAt})"


class SearchQuery(Base):
    __tablename__ = 'query'

    id = Column(String(50), primary_key=True)
    sqlRecord = Column(Text)
    description = Column(String(255))
    datasetUrn = Column(String(255))
    cornJob = Column(String(50))
    totalCount = Column(Integer)
    dailyGrowth = Column(Integer)
    catalog = Column(String(20))
    createdAt = Column(DateTime, server_default=func.now(), comment='创建时间')
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def __repr__(self):
        return f"Query(id={self.id}, sqlRecord={self.sqlRecord}, description={self.description}, " \
               f"datasetUrn={self.datasetUrn}, " \
               f"createdAt={self.createdAt}, updatedAt={self.updatedAt}, cornJob={self.cornJob}, " \
               f"totalCount={self.totalCount}, " \
               f"dailyGrowth={self.dailyGrowth})"


class QueryHistory(Base):
    __tablename__ = 'query_history'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增整数类型id')
    queryId = Column(String(50))
    sqlRecord = Column(Text)
    totalCount = Column(Integer)
    dailyGrowth = Column(Integer)
    catalog = Column(String(20))
    createdAt = Column(DateTime, server_default=func.now(), comment='创建时间')
    recordedAt = Column(DateTime, server_default=func.now(), comment='记录时间')

    def __repr__(self):
        return f"Query(id={self.id}, sqlRecord={self.sqlRecord}, description={self.description}, " \
               f"datasetUrn={self.datasetUrn}, " \
               f"createdAt={self.createdAt}, updatedAt={self.updatedAt}, cornJob={self.cornJob}, " \
               f"totalCount={self.totalCount}, " \
               f"dailyGrowth={self.dailyGrowth})"


class DIKubeQuery(Base):
    __tablename__ = 'dikube_query'

    dikubeId = Column(String(50), ForeignKey('dikube.id'), primary_key=True)
    queryId = Column(String(50), ForeignKey('query.id'), primary_key=True)

    def __repr__(self):
        return f"DIKubeQuery(dikubeId={self.dikubeId}, queryId={self.queryId})"