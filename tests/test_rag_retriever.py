from __future__ import annotations

import unittest

from llm.rag.models import DocumentChunk
from llm.rag.retriever import SimpleKeywordRetriever, tokenize


class RagRetrieverTestCase(unittest.TestCase):
    def test_tokenize_contains_chinese_and_english(self) -> None:
        tokens = tokenize("Android 启动优化 startup")
        self.assertIn("android", tokens)
        self.assertIn("启", tokens)
        self.assertIn("startup", tokens)

    def test_retrieve_returns_relevant_chunk_first(self) -> None:
        retriever = SimpleKeywordRetriever(
            [
                DocumentChunk(
                    chunk_id="1",
                    source_id="a",
                    title="architecture",
                    content="Android 架构设计强调模块化和分层。",
                ),
                DocumentChunk(
                    chunk_id="2",
                    source_id="b",
                    title="performance",
                    content="启动优化要先看 Application 初始化和首屏请求。",
                ),
            ]
        )

        results = retriever.retrieve("Android 启动优化", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].chunk.title, "performance")


if __name__ == "__main__":
    unittest.main()
