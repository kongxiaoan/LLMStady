from __future__ import annotations

from llm.rag.models import DocumentChunk, SourceDocument


def chunk_documents(
    documents: list[SourceDocument],
    *,
    chunk_size: int = 360,
    overlap: int = 60,
) -> list[DocumentChunk]:
    """把文档按固定窗口切分。

    这是最基础的 chunk 策略。
    真实项目中可以换成：
    - 语义分段
    - 标题分段
    - 代码块感知分段
    - LangChain text splitter
    """

    chunks: list[DocumentChunk] = []
    step = max(1, chunk_size - overlap)

    for document in documents:
        content = document.content.strip()
        if not content:
            continue

        for index, start in enumerate(range(0, len(content), step)):
            piece = content[start : start + chunk_size].strip()
            if not piece:
                continue
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{document.source_id}-chunk-{index}",
                    source_id=document.source_id,
                    title=document.title,
                    content=piece,
                )
            )

    return chunks
