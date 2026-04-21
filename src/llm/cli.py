from __future__ import annotations

import argparse
from dataclasses import asdict

from llm.agent.runner import MobileArchitectAssistant
from llm.domain.models import RuntimeContext


# 这个文件专注于处理命令行输入输出，保持逻辑清晰，便于后续扩展。
def build_parser() -> argparse.ArgumentParser:
    """集中定义 CLI 参数，方便后续扩展命令行能力。"""

    parser = argparse.ArgumentParser(
        description="专家级移动端架构 Agent，基于 LangChain + DeepSeek。"
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="你想咨询 Agent 的问题；如果不传，程序会进入交互输入。",
    )
    parser.add_argument("--thread-id", help="会话线程 ID，用于保持多轮上下文。")
    parser.add_argument(
        "--platform",
        default="android",
        help="目标平台，例如 android / ios / flutter / react-native。",
    )
    parser.add_argument(
        "--experience",
        default="intermediate",
        help="你的经验层级，例如 junior / intermediate / senior。",
    )
    parser.add_argument(
        "--language",
        default="java",
        help="你当前最关注的语言，例如 java / kotlin / swift。",
    )
    parser.add_argument(
        "--user-name",
        default="Zhuanz",
        help="上下文里的用户名，仅用于演示 context_schema。",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="输出原始结构化结果，适合你调试 LangChain 响应。",
    )
    return parser


def _build_context(args: argparse.Namespace) -> RuntimeContext:
    return RuntimeContext(
        user_name=args.user_name,
        target_platform=args.platform,
        experience_level=args.experience,
        preferred_language=args.language,
    )


def _print_response(response: object, *, raw: bool) -> None:
    if raw:
        print(asdict(response))
        return

    print("=== 核心结论 ===")
    print(response.summary)
    print()
    print("=== 架构建议 ===")
    print(response.architecture_recommendation)
    print()
    print("=== 性能建议 ===")
    print(response.performance_recommendation)
    print()
    print("=== 设计原则 ===")
    print(response.design_principles)
    print()
    print("=== 风险提醒 ===")
    for item in response.risks:
        print(f"- {item}")
    print()
    print("=== 学习要点 ===")
    for item in response.learning_notes:
        print(f"- {item}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # 对学习项目来说，允许不传问题后再输入，交互体验会更友好。
    question = args.question or input("请输入你想咨询的问题: ").strip()
    if not question:
        raise SystemExit("问题不能为空。")

    assistant = MobileArchitectAssistant()
    response = assistant.ask(
        question=question,
        context=_build_context(args),
        thread_id=args.thread_id,
    )
    _print_response(response, raw=args.raw)
