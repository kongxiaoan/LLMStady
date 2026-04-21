from __future__ import annotations

from langchain.tools import tool


def generate_architecture_advice(
    platform: str,
    project_type: str,
    team_size: str,
) -> str:
    """返回架构建议。

    这里故意保留一定的规则引擎风格，而不是把所有知识都交给模型。
    这样你可以看到：在真实工程中，LLM 往往和“确定性业务规则”混合使用。
    """

    normalized_platform = platform.lower()
    normalized_type = project_type.lower()
    normalized_team_size = team_size.lower()

    architecture = "分层架构 + 模块化"
    if normalized_platform == "android":
        architecture = "Clean Architecture + MVVM + Feature 模块化"
    elif normalized_platform == "ios":
        architecture = "Clean Architecture + Coordinator + 模块边界治理"
    elif normalized_platform == "flutter":
        architecture = "Feature-first 分层 + Riverpod/BLoC + 包级模块化"
    elif normalized_platform in {"react-native", "rn"}:
        architecture = "业务模块分层 + 原生桥接边界治理 + 状态管理统一"

    collaboration = "中小团队可先以单仓 + 明确模块边界推进。"
    if normalized_team_size in {"large", "enterprise", "50+"}:
        collaboration = "大团队建议采用多模块治理、统一脚手架、接口契约和架构守卫。"

    evolution = "优先保证可演进性，而不是过早追求复杂抽象。"
    if "super" in normalized_type or "平台" in normalized_type:
        evolution = "超级 App / 平台型项目要优先考虑插件化、能力下沉和稳定 API 边界。"
    elif "im" in normalized_type or "实时" in normalized_type:
        evolution = "实时业务需优先设计消息状态一致性、离线缓存与弱网补偿机制。"

    return (
        f"推荐架构：{architecture}\n"
        f"协作建议：{collaboration}\n"
        f"演进重点：{evolution}\n"
        "落地顺序：先划分 domain / application / infrastructure 边界，"
        "再抽离可复用组件，最后引入架构治理与自动化约束。"
    )


@tool
def architecture_advisor(platform: str, project_type: str, team_size: str) -> str:
    """根据平台、项目类型和团队规模给出移动端架构建议。"""

    return generate_architecture_advice(platform, project_type, team_size)
