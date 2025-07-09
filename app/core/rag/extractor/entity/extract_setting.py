# -*- coding: utf-8 -*-
# @Time    : 2025/07/08 6:26 AM
# @Author  : Galleons
# @File    : extract_setting.py

"""
解析数据模型
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.models.dataset import Document
from app.models.model import UploadFile


class NotionInfo(BaseModel):
    """
    Notion import info.
    """

    notion_workspace_id: str
    notion_obj_id: str
    notion_page_type: str
    document: Optional[Document] = None
    tenant_id: str
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data) -> None:
        super().__init__(**data)


class WebsiteInfo(BaseModel):
    """
    website import info.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    provider: str
    job_id: str
    url: str
    mode: str
    tenant_id: str
    only_main_content: bool = False


class ExtractSetting(BaseModel):
    """
    Model class for provider response.
    """

    datasource_type: str
    upload_file: Optional[UploadFile] = None
    notion_info: Optional[NotionInfo] = None
    website_info: Optional[WebsiteInfo] = None
    document_model: Optional[str] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data) -> None:
        super().__init__(**data)
