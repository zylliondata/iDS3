# 中云开源数据技术（上海）有限公司 工业数据去中心化分布式共生共享空间(iDS3)

> 中云开源数据技术（上海）有限公司,以下简称为中云数据


中云数据 iDS3(industrial Data Decentralized Distributed Symbiotic Sharing Space)是一个开源的数据管理平台。 它集成了 Data Fabric、Data Mesh 和 Data Space（我们称之为“3D 概念”）的概念和优点。
现在, 该存储库只是 iDS3 的一个子项目案例示意，即 ioDS3，它专注于开放/Web 数据的管理，以展示 iDS3 的基本架构。

iDS3 拥有但 ioDS3 没有的功能:

1. 数据产品集成
2. 数据共享和传输。

当前这个示例项目仅支持三种数据源 : MariaDB, MongoDB, 以及 Deltalake；未来，我们将开源更多与iDS3产品系列相关的产品或Demo。


[![License](https://img.shields.io/badge/license-Apache%202-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

## 特性

- 可以支持任意应用场景下的多源异构数据的集成和开箱即用。
- 提供一个可扩展、灵活的平台来连接各个系统中孤立的数据并在整个组织内提供可供分析的集成数据。
- 使用元数据驱动的方法来索引、发现和组织来自不同来源的数据。
- 采用数据网格的架构，将数据平台分解为自治团队拥有的独立域。
- 面向场景的去中心化、分布式数据所有权和平台思维，可以从数据中创造更多价值。
- 利用工业机理构建知识图谱，进行元数据的富化。

## 开源组件依赖

- [Spark](https://github.com/apache/spark)
- [DeltaLake](https://github.com/delta-io/delta)
- [Datahub](https://github.com/datahub-project/datahub)
- [Trino](https://github.com/trinodb/trino)
- [MariaDB](https://github.com/MariaDB/server)
- [Nacos](https://github.com/alibaba/nacos)
- [FastAPI](https://github.com/tiangolo/fastapi)

## 构建方式

- 第一步, MariaDB, DataHub, Trino 和 Nacos 需要提前部署
- 第二步,执行 `init.sql` 初始化MariaDB数据库
- 第三步,在此py 文件中 `./src/config.py` 配置Nacos 连接信息
- 第四步, 从Nacos Server 获取对应的配置, 配置模版如下：

```json
{
  "datahub": {
    "server": "http://xxx:8080",
    "ui": "http://xxx:9002",
    "route": "/api/graphql",
    "timeout_sec": 30,
    "disable_ssl_verification": false,
    "token": "xxx"
  },
  "mariadb": {
    "host": "xxx",
    "port": "3306",
    "user": "xxx",
    "pwd": "xxx",
    "db": "iDS3"
  },
  "trino": {
    "host": "xxx",
    "port": 8443,
    "user": "admin",
    "catalog": "",
    "auth_user": "xxx",
    "auth_pwd": "xxx",
    "http_scheme": "https",
    "verify": false
  }
}
```

## 使用方式

> Docker and Docker Compose 是必要的

拉取项目到本地目录, 执行 `docker compose build --no-cache`, 进行构建; 然后执行 `docker compose up -d`,启动项目。

可以进行在线API的浏览:  `xxx:8080/docs`

## 反馈和支持

如果您有任何反馈或功能请求，请随时在此存储库上提出问题。我们非常感谢您的反馈，以使该项目更加繁荣的发展！

如需针对您的使用案例的优先支持和定制，请联系我们
 [info@zylliondata.com]([mailto:info@zylliondata.com](mailto:info@zylliondata.com)).




