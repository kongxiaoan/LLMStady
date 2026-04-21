from __future__ import annotations

from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from llm.config import Settings
from llm.domain.models import ExpertAnswer, RuntimeContext
from llm.prompts.system_prompt import SYSTEM_PROMPT
from llm.tools import MOBILE_EXPERT_TOOLS


def build_chat_model(settings: Settings) -> ChatDeepSeek:
    """创建模型实例。

    这里直接使用 ChatDeepSeek，而不是走 OpenAI 兼容入口，
    是为了让项目的意图更明确：这是一个 DeepSeek 专用学习示例。
    """

    return ChatDeepSeek(
        model=settings.model,
        api_key=settings.api_key,
        base_url=settings.base_url,
        temperature=settings.temperature,
        max_retries=settings.max_retries,
    )


def build_checkpointer() -> InMemorySaver:
    """创建内存版 checkpoint。

    学习阶段先用 InMemorySaver 最简单；
    真正生产环境可以替换为 Redis、数据库或文件持久化存储。
    """

    serializer = JsonPlusSerializer(
        allowed_msgpack_modules=[
            ("llm.domain.models", "ExpertAnswer"),
            ("llm.domain.models", "RuntimeContext"),
        ]
    )
    return InMemorySaver(serde=serializer)


def build_mobile_architect_agent(settings: Settings):
    model = build_chat_model(settings)

    return create_agent(
        model=model,
        tools=MOBILE_EXPERT_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        response_format=ExpertAnswer,
        context_schema=RuntimeContext,
        checkpointer=build_checkpointer(),
        debug=settings.debug,
        name="mobile-architect-agent",
    )
