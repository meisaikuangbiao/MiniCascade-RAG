from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)

from app.pipeline.feature_pipeline.config import settings


def chunk_text(text: str) -> list[str]:
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n"], chunk_size=500, chunk_overlap=0
    )
    text_split = character_splitter.split_text(text)

    token_splitter = SentenceTransformersTokenTextSplitter(
        chunk_overlap=50,
        tokens_per_chunk=settings.EMBEDDING_MODEL_MAX_INPUT_LENGTH,
        model_name="BAAI/bge-m3",
    )
    chunks = []

    for section in text_split:
        chunks.extend(token_splitter.split_text(section))

    return chunks




def main():
    pass



if __name__ == "__main__":
    main()