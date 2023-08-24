# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 10:21 2023/8/11
# @Description: 数据库配置
# @Version: Python 3.8.11
# @Modified By:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import ioDS3_config

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://%s:%s@%s:%s/%s" % (
    ioDS3_config["mariadb"]["user"],
    ioDS3_config["mariadb"]["pwd"],
    ioDS3_config["mariadb"]["host"],
    ioDS3_config["mariadb"]["port"],
    ioDS3_config["mariadb"]["db"]
)

engine = create_engine(
    # echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
    SQLALCHEMY_DATABASE_URL, echo=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本映射类
Base = declarative_base()

if __name__ == '__main__':
    print(SQLALCHEMY_DATABASE_URL)
