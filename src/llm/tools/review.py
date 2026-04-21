from __future__ import annotations

from langchain.tools import tool


def build_review_checklist(platform: str, focus: str) -> str:
    normalized_platform = platform.lower()
    normalized_focus = focus.lower()

    base_items = [
        "模块边界是否清晰，是否出现跨层直接依赖。",
        "业务逻辑是否混入 UI 层，是否影响可测试性。",
        "异常处理、日志、埋点是否成体系。",
    ]

    if normalized_platform == "android":
        base_items.extend(
            [
                "是否存在 Context 泄漏、ViewModel 滥用或生命周期感知缺失。",
                "列表滚动场景是否避免在主线程做重计算与大对象创建。",
            ]
        )
    elif normalized_platform == "ios":
        base_items.extend(
            [
                "是否存在主线程阻塞、过重布局计算与不必要的 retain cycle 风险。",
                "页面跳转和协调逻辑是否与 ViewController 职责分离。",
            ]
        )

    if "性能" in focus or "performance" in normalized_focus:
        base_items.append("是否有启动、卡顿、内存、耗电等指标和对应监控。")
    if "架构" in focus or "architecture" in normalized_focus:
        base_items.append("是否有稳定抽象层与可演进的扩展点，避免过度耦合。")

    return "\n".join(f"- {item}" for item in base_items)


@tool
def code_review_checklist_builder(platform: str, focus: str) -> str:
    """生成移动端代码评审 checklist。"""

    return build_review_checklist(platform, focus)
