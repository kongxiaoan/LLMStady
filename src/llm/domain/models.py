from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RuntimeContext:
    """运行时上下文。

    context_schema 是 LangChain v1 create_agent 的重要能力：
    它允许你把“用户画像 / 环境信息 / 会话元数据”以结构化方式传给 Agent，
    比起把这些信息硬塞进 prompt，更适合工程项目。
    """

    user_name: str
    target_platform: str
    experience_level: str
    preferred_language: str


@dataclass
class ExpertAnswer:
    """结构化输出。

    使用结构化输出而不是纯文本，有两个工程价值：
    1. 更稳定，后续更容易接前端、接口层、日志系统。
    2. 便于你观察 LLM 输出如何约束成固定字段。
    """

    summary: str
    architecture_recommendation: str
    performance_recommendation: str
    design_principles: str
    risks: list[str] = field(default_factory=list)
    learning_notes: list[str] = field(default_factory=list)
