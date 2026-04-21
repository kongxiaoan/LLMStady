from __future__ import annotations

from dataclasses import asdict
from functools import lru_cache

from fastapi import FastAPI

from llm.agent.runner import MobileArchitectAssistant
from llm.domain.models import RuntimeContext
from llm.http.schemas import AskExpertRequest, AskExpertResponse


@lru_cache(maxsize=1)
def get_assistant() -> MobileArchitectAssistant:
    """缓存 Agent 实例。

    Agent 初始化会读取配置、创建模型与工具图。
    对服务进程来说，这类对象一般做成单例更合理，避免每个请求重复初始化。
    """

    return MobileArchitectAssistant()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Mobile Architect Agent API",
        version="0.1.0",
        description="基于 LangChain + DeepSeek 的移动端专家 Agent HTTP 服务。",
    )

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/mobile-architect/ask", response_model=AskExpertResponse)
    def ask_expert(request: AskExpertRequest) -> AskExpertResponse:
        assistant = get_assistant()
        answer = assistant.ask(
            question=request.question,
            context=RuntimeContext(
                user_name=request.user_name,
                target_platform=request.target_platform,
                experience_level=request.experience_level,
                preferred_language=request.preferred_language,
            ),
            thread_id=request.thread_id,
        )

        # 领域层使用 dataclass，HTTP 层返回 Pydantic；
        # asdict 可以把 dataclass 快速转换成可序列化 dict。
        return AskExpertResponse(**asdict(answer))

    return app


app = create_app()
