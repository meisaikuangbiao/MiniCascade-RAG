# -*- coding: utf-8 -*-
# @Time    : 2025/06/18 3:31 AM
# @Author  : Galleons
# @File    : chatbot_v2.py

"""
这里是文件说明
"""
import gradio as gr
from gradio import ChatMessage
from typing import Iterator
from openai import OpenAI
from app.pipeline.inference_pipeline.config import settings
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
            model=settings.Silicon_model_v1,
            api_key=settings.Silicon_api_key3,
            base_url=settings.Silicon_base_url,
        )




def stream_response(user_message: str, messages: list) -> Iterator[list]:
    """
    Streams both thoughts and responses from the Gemini model.
    """
    # Initialize response from Gemini
    response = model.generate_content(user_message, stream=True)

    # Initialize buffers
    thought_buffer = ""
    response_buffer = ""
    thinking_complete = False

    # Add initial thinking message
    messages.append(
        ChatMessage(
            role="assistant",
            content="",
            metadata={"title": "⏳Thinking: *The thoughts produced by the Gemini2.0 Flash model are experimental"}
        )
    )

    for chunk in response:
        parts = chunk.candidates[0].content.parts
        current_chunk = parts[0].text

        if len(parts) == 2 and not thinking_complete:
            # Complete thought and start response
            thought_buffer += current_chunk
            messages[-1] = ChatMessage(
                role="assistant",
                content=thought_buffer,
                metadata={"title": "⏳Thinking: *The thoughts produced by the Gemini2.0 Flash model are experimental"}
            )

            # Add response message
            messages.append(
                ChatMessage(
                    role="assistant",
                    content=parts[1].text
                )
            )
            thinking_complete = True

        elif thinking_complete:
            # Continue streaming response
            response_buffer += current_chunk
            messages[-1] = ChatMessage(
                role="assistant",
                content=response_buffer
            )

        else:
            # Continue streaming thoughts
            thought_buffer += current_chunk
            messages[-1] = ChatMessage(
                role="assistant",
                content=thought_buffer,
                metadata={"title": "⏳Thinking: *The thoughts produced by the Gemini2.0 Flash model are experimental"}
            )

        yield messages
