from __future__ import annotations

from pydantic import BaseModel, Field


class AskExpertRequest(BaseModel):
    """HTTP 请求模型。

    使用 Pydantic 的好处：
    1. 自动校验请求字段。
    2. 自动生成 OpenAPI 文档。
    3. 让 HTTP 层和领域层的边界更清晰。
    """

    question: str = Field(..., min_length=1, description="用户问题")
    thread_id: str | None = Field(default=None, description="会话线程 ID")
    user_name: str = Field(default="Zhuanz", description="用户名")
    target_platform: str = Field(default="android", description="目标平台")
    experience_level: str = Field(default="intermediate", description="经验等级")
    preferred_language: str = Field(default="java", description="语言偏好")


class AskExpertResponse(BaseModel):
    """HTTP 响应模型，与 Go 侧 proto 字段保持一致。"""

    summary: str
    architecture_recommendation: str
    performance_recommendation: str
    design_principles: str
    risks: list[str]
    learning_notes: list[str]
