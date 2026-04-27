from __future__ import annotations

import argparse
from pathlib import Path

from llm.rag.service import RagDemoService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="项目内 RAG Demo。")
    parser.add_argument("question", help="要查询的问题")
    parser.add_argument("--top-k", type=int, default=3, help="返回前几个检索片段")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="知识库目录，默认使用 docs/rag_demo",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    service = RagDemoService(data_dir=args.data_dir)
    result = service.ask(args.question, top_k=args.top_k)

    print("=== 检索片段 ===")
    for item in result.retrieved_chunks:
        print(f"- [{item.chunk.title}] score={item.score:.2f}")
    print()
    print("=== 回答 ===")
    print(result.answer)
