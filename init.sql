/**
**  中云开源数据技术（上海）有限公司 iDS3-ioDS3 demo
**/

CREATE DATABASE iDS3
  CHARACTER SET utf8
  COLLATE utf8_general_ci
  DEFAULT CHARSET=utf8
  DEFAULT COLLATE=utf8_general_ci;

USE iDS3;

CREATE TABLE data_source (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '数据源唯一标识',
    sourceUrn VARCHAR(100) UNIQUE NOT NULL COMMENT '数据源Urn',
    sourceType VARCHAR(20) COMMENT '数据源类型',
    sourceName VARCHAR(50) COMMENT '数据源名称',
    sourceRecipe TEXT COMMENT '数据源配置',
    executionRequestUrn VARCHAR(100) COMMENT '数据源执行请求Urn',
    executionResultStatus VARCHAR(10) COMMENT '数据源执行结果状态',
    executionResultStartTimeMs BIGINT COMMENT '数据源执行结果开始时间',
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

ALTER TABLE data_source
ORDER BY executionResultStartTimeMs;

CREATE TABLE file_info (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增整数类型id',
    savePath VARCHAR(255) COMMENT '文件MINIO保存路径',
    trinoPath VARCHAR(255) COMMENT 'TRINO保存路径',
    description TEXT COMMENT '文件描述',
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE dikube (
    id VARCHAR(50) PRIMARY KEY,
    description VARCHAR(255),
    userID VARCHAR(255),
    project VARCHAR(20),
    dikubeId VARCHAR(50),
    status BOOLEAN,
    name VARCHAR(20),
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE query (
    id VARCHAR(50) PRIMARY KEY,
    sqlRecord TEXT,
    description VARCHAR(255),
    datasetUrn VARCHAR(255),
    cornJob VARCHAR(50),
    totalCount INT,
    dailyGrowth INT,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE dikube_query (
    dikubeId VARCHAR(50),
    queryId VARCHAR(50),
    PRIMARY KEY (dikubeId, queryId),
    FOREIGN KEY (dikubeId) REFERENCES dikube(id),
    FOREIGN KEY (queryId) REFERENCES query(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE query_history (
  id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '自增整数类型id',
  queryId VARCHAR(50),
  sqlRecord TEXT,
  totalCount INTEGER,
  dailyGrowth INTEGER,
  catalog VARCHAR(20),
  createdAt DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  recordedAt DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间'
);
