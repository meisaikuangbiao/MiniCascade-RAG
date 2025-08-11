# -*- coding: utf-8 -*-
# @Time   : 2025/8/11 15:51
# @Author : Galleons
# @File   : db_config.py

"""
数据库连接配置
"""

from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, TomlConfigSettingsSource

class PostgresConfig(BaseSettings):

    DEBUG: bool = True
    POSTGRES_DATABASE_HOST: str = 'localhost'
    POSTGRES_DATABASE_PORT: int = 5432
    TIMESCALE_URL: str | None = None
