from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SourceDocument:
    """原始知识文档。"""

    source_id: str
    title: str
    content: str


@dataclass
class DocumentChunk:
    """切分后的文档块。

    在 RAG 中，原始文档通常不会直接整体送入模型，而是先切分成 chunk，
    这样检索粒度更细，也更容易控制上下文长度。
    """

    chunk_id: str
    source_id: str
    title: str
    content: str


@dataclass
class RetrievedChunk:
    """检索结果。"""

    chunk: DocumentChunk
    score: float
