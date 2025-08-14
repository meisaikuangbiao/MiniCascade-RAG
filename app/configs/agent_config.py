# -*- coding: utf-8 -*-
# @Time   : 2025/8/13 17:39
# @Author : Galleons
# @File   : agent_config.py

"""
这里是文件说明
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = str(Path(__file__).parent.parent.parent)+'/.env'


class AgentConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR, env_file_encoding="utf-8", extra='ignore')

