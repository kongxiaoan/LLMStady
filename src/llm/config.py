from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Final

from dotenv import load_dotenv


DEFAULT_BASE_URL: Final[str] = "https://api.deepseek.com"
DEFAULT_MODEL: Final[str] = "deepseek-chat"
DEFAULT_THREAD_ID: Final[str] = "mobile-architect-thread"


@dataclass
class Settings:
    """项目运行配置。

    使用 dataclass 的原因：
    1. 让配置字段具备清晰的类型定义。
    2. 避免到处传散乱的 dict，提升可维护性。
    3. 对初学者来说，可读性比手写 __init__ 更高。
    """

    api_key: str
    base_url: str
    model: str
    temperature: float
    max_retries: int
    default_thread_id: str
    debug: bool
    http_host: str
    http_port: int

    def validate(self) -> None:
        """在应用启动早期做配置校验，尽量把错误前置。"""

        if not self.api_key or self.api_key == "your_deepseek_api_key_here":
            raise ValueError("请先在 .env 中配置有效的 DEEPSEEK_API_KEY。")

        # 官方文档指出 deepseek-reasoner 当前不支持工具调用与结构化输出。
        # 本项目是 Agent 项目，依赖这两项能力，因此默认只接受 deepseek-chat。
        if self.model == "deepseek-reasoner":
            raise ValueError(
                "deepseek-reasoner 当前不支持工具调用/结构化输出，"
                "本项目请使用 deepseek-chat。"
            )


def _read_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _read_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return int(value)


def _read_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return float(value)


def load_settings() -> Settings:
    # load_dotenv 会把 .env 中的配置加载到当前进程环境变量里。
    # 这样后续逻辑统一通过 os.getenv 读取，结构更清晰。
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    base_url = os.getenv("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL).strip()
    model = os.getenv("DEEPSEEK_MODEL", DEFAULT_MODEL).strip()

    settings = Settings(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=_read_float("APP_TEMPERATURE", 0.0),
        max_retries=_read_int("APP_MAX_RETRIES", 2),
        default_thread_id=os.getenv("APP_DEFAULT_THREAD_ID", DEFAULT_THREAD_ID).strip()
        or DEFAULT_THREAD_ID,
        debug=_read_bool("APP_DEBUG", False),
        http_host=os.getenv("APP_HTTP_HOST", "127.0.0.1").strip() or "127.0.0.1",
        http_port=_read_int("APP_HTTP_PORT", 8080),
    )
    settings.validate()
    return settings
