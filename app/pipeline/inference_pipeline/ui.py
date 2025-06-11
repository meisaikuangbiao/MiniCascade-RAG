import sys
from pathlib import Path

# 为了模拟使用多个Python模块，如'core'和'feature_pipeline'，
# 我们将'./src'目录添加到PYTHONPATH中。这不适用于生产环境，
# 仅用于开发和教学目的。
ROOT_DIR = str(Path(__file__).parent.parent)
sys.path.append(ROOT_DIR)

from app.core.config import settings
from reasoning import ReasoningPipeline

settings.patch_localhost()


import gradio as gr
from app.pipeline.inference_pipeline.reasoning import ReasoningPipeline

llm_twin = ReasoningPipeline(mock=False)


def predict(message: str, history: list[list[str]], author: str) -> str:
    """
    使用KunlunRAG 深度思考助手生成回复，模拟与你的深度思考助手的对话。

    参数：
        message (str): 用户的输入消息或问题。
        history (List[List[str]]): 用户和KunlunRAG之间的历史对话记录。
        about_me (str): 关于用户的个人上下文，用于个性化回复。

    返回：
        str: KunlunRAG生成的回复。
    """

    query = f"我是{author}。请写关于：{message}"
    response = llm_twin.generate(
        query=query, enable_rag=True, sample_for_evaluation=False
    )

    return response["answer"]


demo = gr.ChatInterface(
    predict,
    textbox=gr.Textbox(
        placeholder="与你的KunlunRAG聊天",
        label="消息",
        container=False,
        scale=7,
    ),
    additional_inputs=[
        gr.Textbox(
            "张三",
            label="你是谁？",
        )
    ],
    title="你的KunlunRAG",
    description="""
    与你的个性化KunlunRAG聊天！这个AI助手将帮助你创作内容，融入你的风格和语气。
    """,
    theme="soft",
    examples=[
        [
            "写一篇关于RAG系统的文章。",
            "张三",
        ],
        [
            "写一段关于向量数据库的文章段落。",
            "张三",
        ],
        [
            "写一篇关于LLM聊天机器人的文章。",
            "张三",
        ],
    ],
    cache_examples=False,
)


if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=True)
