from __future__ import annotations

from langchain.tools import ToolRuntime, tool

from llm.domain.models import RuntimeContext


@tool
def runtime_profile_reader(runtime: ToolRuntime[RuntimeContext]) -> str:
    """读取当前用户上下文。

    这个工具主要用于演示 `ToolRuntime[Context]` 的用法：
    Agent 在调用工具时可以拿到结构化上下文，而不是只看用户问题文本。
    """

    context = runtime.context
    return (
        f"当前用户是 {context.user_name}，"
        f"经验层级为 {context.experience_level}，"
        f"关注平台为 {context.target_platform}，"
        f"偏好语言为 {context.preferred_language}。"
    )
