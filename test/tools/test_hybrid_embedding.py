# -*- coding: utf-8 -*-
# @Time    : 2025/06/18 6:28 AM
# @Author  : Galleons
# @File    : test_hybrid_embedding.py

"""
这里是文件说明
"""


import os
os.environ['CUDA_VISIBLE_DEVICES'] = '2'



from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel('/data/model_cache/bge-m3', use_fp16=True)

sentences = ["What is BGE M3?", "Defination of BM25"]

