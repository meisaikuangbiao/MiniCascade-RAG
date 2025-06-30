# -*- coding: utf-8 -*-
# @Time    : 2025/06/19 3:33 AM
# @Author  : Galleons
# @File    : test_response.py

"""
这里是文件说明
"""

import pytest
from app.pipeline.inference_pipeline.reasoning import ReasoningPipeline

inference_endpoint = ReasoningPipeline(mock=False)

query = """
        你好，我是张三。

        你能帮我写一段关于RAG的文章段落吗？
        我特别感兴趣的是如何设计一个RAG系统。
    """

response = inference_endpoint.generate(
    query=query, enable_rag=True, sample_for_evaluation=True, doc_names=['test_doc']
)

def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5