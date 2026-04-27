from __future__ import annotations

from pathlib import Path

from llm.rag.models import SourceDocument


def load_documents(data_dir: Path) -> list[SourceDocument]:
    """从本地目录读取知识文档。

    这里故意使用最朴素的本地文件加载方式，目的是帮助理解 RAG 的最小闭环：
    文档 -> 切分 -> 检索 -> 生成。
    """

    documents: list[SourceDocument] = []
    for path in sorted(data_dir.glob("*.md")):
        documents.append(
            SourceDocument(
                source_id=path.stem,
                title=path.stem.replace("_", " "),
                content=path.read_text(encoding="utf-8"),
            )
        )
    return documents
