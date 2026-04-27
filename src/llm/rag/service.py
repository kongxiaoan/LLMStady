from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from langchain_deepseek import ChatDeepSeek

from llm.config import load_settings
from llm.rag.chunker import chunk_documents
from llm.rag.loader import load_documents
from llm.rag.models import RetrievedChunk
from llm.rag.retriever import SimpleKeywordRetriever


DEFAULT_DATA_DIR = Path(__file__).resolve().parents[3] / "docs" / "rag_demo"


@dataclass
class RagAnswer:
    answer: str
    retrieved_chunks: list[RetrievedChunk]


class RagDemoService:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.settings = load_settings()
        self.data_dir = data_dir or DEFAULT_DATA_DIR

        documents = load_documents(self.data_dir)
        chunks = chunk_documents(documents)
        self.retriever = SimpleKeywordRetriever(chunks)
        self.model = ChatDeepSeek(
            model=self.settings.model,
            api_key=self.settings.api_key,
            base_url=self.settings.base_url,
            temperature=0,
            max_retries=self.settings.max_retries,
        )

    def ask(self, question: str, *, top_k: int = 3) -> RagAnswer:
        retrieved_chunks = self.retriever.retrieve(question, top_k=top_k)
        context = self._build_context(retrieved_chunks)

        response = self.model.invoke(
            [
                (
                    "system",
                    "你是一个移动端技术知识库问答助手。"
                    "必须优先基于提供的检索上下文回答。"
                    "如果上下文不足以支持明确结论，要直接说明“知识库上下文不足”。",
                ),
                (
                    "human",
                    f"问题：{question}\n\n"
                    f"检索上下文：\n{context}\n\n"
                    "请给出结构清晰的中文回答，并明确引用到哪些知识点。",
                ),
            ]
        )
        return RagAnswer(answer=response.content or "", retrieved_chunks=retrieved_chunks)

    def _build_context(self, retrieved_chunks: list[RetrievedChunk]) -> str:
        if not retrieved_chunks:
            return "没有检索到相关知识。"

        parts: list[str] = []
        for index, item in enumerate(retrieved_chunks, start=1):
            parts.append(
                f"[片段{index}] 标题={item.chunk.title} 分数={item.score:.2f}\n{item.chunk.content}"
            )
        return "\n\n".join(parts)
