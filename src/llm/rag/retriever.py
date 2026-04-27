from __future__ import annotations

import math
import re
from collections import Counter

from llm.rag.models import DocumentChunk, RetrievedChunk


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]")


def tokenize(text: str) -> list[str]:
    """简单分词。

    这里不引入额外中文分词依赖，使用“英文单词 + 单个中文字符”的策略做最小 demo。
    它不适合生产，但足够帮助理解 RAG 检索阶段的基本原理。
    """

    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


class SimpleKeywordRetriever:
    """一个本地关键词检索器。

    这里使用简化的 TF 风格打分，不依赖向量数据库。
    目的不是替代专业向量检索，而是让学习阶段更容易看懂“为什么这段被召回”。
    """

    def __init__(self, chunks: list[DocumentChunk]) -> None:
        self._chunks = chunks
        self._token_cache = {chunk.chunk_id: tokenize(chunk.content) for chunk in chunks}

    def retrieve(self, query: str, *, top_k: int = 3) -> list[RetrievedChunk]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        query_counter = Counter(query_tokens)
        results: list[RetrievedChunk] = []

        for chunk in self._chunks:
            chunk_tokens = self._token_cache[chunk.chunk_id]
            if not chunk_tokens:
                continue

            chunk_counter = Counter(chunk_tokens)
            score = 0.0

            for token, query_count in query_counter.items():
                if token not in chunk_counter:
                    continue

                # 这里用一个简单的对数 TF 打分，减少高频词对结果的过度影响。
                score += (1.0 + math.log(chunk_counter[token])) * query_count

            if score <= 0:
                continue

            results.append(RetrievedChunk(chunk=chunk, score=score))

        results.sort(key=lambda item: item.score, reverse=True)
        return results[:top_k]
