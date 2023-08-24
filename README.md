# Zylliondata iDS3 (industrial Data Decentralized Distributed Symbiotic Sharing Space)

See the [中文文档](https://github.com/zylliondata/iDS3/blob/main/README-zh.md) for Chinese readme.

Zylliondata iDS3(industrial Data Decentralized Distributed Symbiotic Sharing Space) is a open-sourced data management platform. It integrates the concepts and benefits of Data Fabric, Data Mesh, and Data Space, or "3D Concepts" as we call it.
For now, this repository is merely a sub-set of iDS3, namely ioDS3, which focuses on management of open/web data, to showcase the basic architecture of iDS3. 

Features that iDS3 has but ioDS3 not:

1. Integrated data product
2. Data Sharing and transferring.

Now this project only supports three types of data sources: MariaDB, MongoDB, and Deltalake. In the future, We will open source more products or demos related to the iDS3 product series.


[![License](https://img.shields.io/badge/license-Apache%202-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

## Features

- can realize the out-of-the-box integration of multi-source heterogeneous data in any application scenario.
- provides a scalable, flexible platform to unlock siloed data and deliver analytics-ready, integrated data across the
  organization.
- uses a metadata-driven approach to index, discover and organize data from disparate sources
- adopt a data mesh paradigm that decomposes the data platform into self-contained domains owned by autonomous teams
- domain-oriented decentralization, distributed data ownership and platform thinking to deliver more value from our data
- a knowledge graph is constructed using industrial mechanism to enrich the metadata;

## Open Source Components

- [Spark](https://github.com/apache/spark)
- [DeltaLake](https://github.com/delta-io/delta)
- [Datahub](https://github.com/datahub-project/datahub)
- [Trino](https://github.com/trinodb/trino)
- [MariaDB](https://github.com/MariaDB/server)
- [Nacos](https://github.com/alibaba/nacos)
- [FastAPI](https://github.com/tiangolo/fastapi)

## How to build

- First, MariaDB, DataHub, Trino and Nacos need to be deployed in advance
- Execute init.sql to initialize the MariaDB database
- Nacos connection information will be obtained from environment variables in `./src/config.py`
- Finally, get the configuration information through Nacos, the instance configuration is as follows

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

## How to Use

> Docker and Docker Compose is necessary

Pull the project to the local directory, execute `docker compose build --no-cache`, to build; then
execute `docker compose up -d`,to start the project.

Browse the APIS at:  `xxx:8080/docs`

## Feedback and Support

If you have any feedback or feature requests, feel free to open an issue on this repository.Your feedback is greatly appreciated to make this project more useful to the community!

For priority support and customizations for your use case, contact us
at [info@zylliondata.com]([mailto:info@zylliondata.com](mailto:info@zylliondata.com)).




