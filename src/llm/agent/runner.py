from __future__ import annotations

from dataclasses import dataclass

from llm.agent.factory import build_mobile_architect_agent
from llm.config import Settings, load_settings
from llm.domain.models import ExpertAnswer, RuntimeContext


@dataclass
class MobileArchitectAssistant:
    """Agent 服务门面。

    这层的作用类似应用服务层：
    - 封装配置加载
    - 封装 Agent 创建
    - 暴露简单稳定的 ask() 接口
    """

    settings: Settings | None = None

    # 在 dataclass 中使用 __post_init__ 来处理复杂的初始化逻辑，例如依赖注入或资源创建。
    def __post_init__(self) -> None:
        self.settings = self.settings or load_settings()
        self.agent = build_mobile_architect_agent(self.settings)

    def ask(
        self,
        question: str,
        context: RuntimeContext,
        thread_id: str | None = None,
    ) -> ExpertAnswer:
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
            config={
                "configurable": {
                    "thread_id": thread_id or self.settings.default_thread_id
                }
            },
            context=context,
        )
        return result["structured_response"]
