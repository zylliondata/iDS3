# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 10:11 2023/8/10
# @Description: Todo
# @Version: Python 3.8.11
# @Modified By:
from typing import Optional

from pydantic import BaseModel, Field


class RequestDIKubeModel(BaseModel):
    id: Optional[str] = Field(None, title="ID", description="ID")
    description: Optional[str] = Field(None, title="描述", description="描述")
    name: str = Field(title="项目名称")
    dikubeId: str = Field(title="DIKube or Catalog ID")
    project: str = Field(default="catalog", title="项目", description="dikube 或者 catalog")

