from setuptools import setup, find_packages


# uv pip install -e .

setup(
    name="kunlunrag",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "bytewax>=0.21.1",
        "gradio>=5.31.0",
        "langchain>=0.3.25",
        "llama-index>=0.12.37",
        "llama-index-vector-stores-qdrant>=0.6.0",
        "pika>=1.3.2",
        "pydantic>=2.11.5",
        "pymongo>=4.13.0",
        "qdrant-client>=1.14.2",
        "structlog>=25.3.0",
    ],
) 


