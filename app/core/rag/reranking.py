from app.core.config import settings
from langchain_openai import ChatOpenAI
from typing import List

from app.core.config import settings
import requests
import json
import os

import app.core.logger_utils as logger_utils
logger = logger_utils.get_logger(__name__)



class Reranker:
    @staticmethod
    def generate_response(
        query: str, passages: list[str], keep_top_k: int
    ) -> list[str]:
        payload = {
            "model": settings.Silicon_model_rerank,
            "query": query,
            "documents": passages,
            "top_n": keep_top_k,
            "return_documents": False,
            "max_chunks_per_doc": 1024,
            "overlap_tokens": 80
        }

        headers = {
            "Authorization": f"Bearer {settings.Silicon_api_key3}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            os.path.join(settings.Silicon_base_url, 'rerank'),
            json=payload,
            headers=headers)
        response_data = json.loads(response.text)

        logger.debug(response_data)
        ranked_indices = [result["index"] for result in response_data["results"]]
        reranked_passages = [passages[idx] for idx in ranked_indices]

        return reranked_passages

if __name__ == "__main__":
    query = "苹果"
    passages = ["苹果", "香蕉", "水果", "蔬菜"]
    keep_top_k = 4
    rerank_passages = Reranker.generate_response(query, passages, keep_top_k)
    print(rerank_passages)
