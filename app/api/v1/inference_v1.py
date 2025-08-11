# -*- coding: utf-8 -*-
# @Time   : 2025/8/4 12:57
# @Author : Galleons
# @File   : inference_v1.py

"""
推理 API 接口
"""

#from app.api.dependency import langfuse
from contextlib import asynccontextmanager
from langfuse.openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langfuse.openai import OpenAI, AsyncOpenAI

import fastapi

load_dotenv()
api_key = os.getenv('API_KEY')

router = APIRouter()


@asynccontextmanager
async def lifespan(_app: fastapi.FastAPI):
    async with Database.connect() as db:
        yield {'db': db}


app = fastapi.FastAPI(lifespan=lifespan)


# Initialize the OpenAI client, pointing it to the DeepSeek Inference API
client = OpenAI(
    base_url="https://api.siliconflow.cn/v1",  # Replace with the DeepSeek model endpoint URL
    api_key=os.getenv('API_KEY'),  # Replace with your DeepSeek API key
)


completion = client.chat.completions.create(
  name="test-chat",
  model="deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
  messages=[
      {"role": "system", "content": "You are a very accurate calculator. You output only the result of the calculation."},
      {"role": "user", "content": "1 + 1 = "}],
  temperature=0,
  metadata={"someMetadataKey": "someValue"},
)

print(completion)

from app.pipeline.inference_pipeline.reasoning import ReasoningPipeline

llm_twin = ReasoningPipeline(mock=False)


def predict(message: str, history: list[list[str]], author: str) -> str:
    """
    使用  深度思考助手生成回复，模拟与你的深度思考助手的对话。

    参数：
        message (str): 用户的输入消息或问题。
        history (List[List[str]]): 用户和Cascade-RAG之间的历史对话记录。
        about_me (str): 关于用户的个人上下文，用于个性化回复。

    返回：
        str: Cascade-RAG生成的回复。
    """

    query = f"我是{author}。请写关于：{message}"
    response = llm_twin.generate(
        query=query, enable_rag=True, sample_for_evaluation=False
    )

    return response["answer"]


