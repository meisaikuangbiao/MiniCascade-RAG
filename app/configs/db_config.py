# -*- coding: utf-8 -*-
# @Time   : 2025/8/11 15:51
# @Author : Galleons
# @File   : db_config.py

"""
数据库连接配置
"""

from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, TomlConfigSettingsSource
from pydantic import PostgresDsn, Field

class PostgresConfig(BaseSettings):

    DEBUG: bool = True
    POSTGRES_DATABASE_HOST: str = 'localhost'
    POSTGRES_DATABASE_PORT: int = 5433
    TIMESCALE_URL: str | None = None

    PG_HOST: str = "localhost"
    PG_PORT: int = 5433
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "postgres"
    PG_DB: str = "mydb"

    # psycopg3 异步
    POSTGRES_URL: PostgresDsn = Field(
        default="postgresql+psycopg://user:pass@localhost:5432/mydb"
    )

    # 连接池
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 20
    POOL_RECYCLE: int = 1800  # 秒，避免空闲连接被中断
    ECHO_SQL: bool = False
    COMMAND_TIMEOUT: float = 5.0  # 秒，asyncpg 全局命令超时

    @property
    def db_url_async(self) -> str:
        return (
            f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}"
            f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
        )

    class Config:
        env_file = ".env"