from __future__ import annotations

from langchain.tools import tool


def diagnose_performance_issue(platform: str, symptom: str) -> str:
    normalized_platform = platform.lower()
    normalized_symptom = symptom.lower()

    baseline = [
        "先建立性能观测体系：启动耗时、FPS、卡顿率、ANR/崩溃率、内存峰值、网络时延。",
        "先验证问题是否可稳定复现，再进入优化，否则容易把时间浪费在伪问题上。",
    ]

    platform_hint = "移动端通用优化策略。"
    if normalized_platform == "android":
        platform_hint = (
            "Android 优先关注主线程阻塞、Bitmap 内存、冷启动链路、RecyclerView 过度绑定。"
        )
    elif normalized_platform == "ios":
        platform_hint = (
            "iOS 优先关注主线程布局、离屏渲染、AutoLayout 复杂度、图片解码与对象生命周期。"
        )

    symptom_hint = "建议按启动、渲染、内存、网络四条主线排查。"
    if "启动" in symptom or "cold" in normalized_symptom:
        symptom_hint = (
            "启动慢通常先查 Application 初始化、首页接口串行等待、首屏资源加载和路由链路。"
        )
    elif "卡顿" in symptom or "fps" in normalized_symptom:
        symptom_hint = "卡顿通常先查主线程重任务、频繁重绘、列表 item 绑定开销和不必要动画。"
    elif "内存" in symptom or "oom" in normalized_symptom:
        symptom_hint = "内存问题优先查大图、缓存失控、生命周期泄漏和对象复用不足。"
    elif "耗电" in symptom or "battery" in normalized_symptom:
        symptom_hint = "耗电问题优先查高频定位、后台轮询、无效唤醒和频繁网络请求。"

    return "\n".join(
        [
            f"平台提示：{platform_hint}",
            f"症状提示：{symptom_hint}",
            "排查基线：",
            *[f"- {item}" for item in baseline],
        ]
    )


@tool
def performance_diagnoser(platform: str, symptom: str) -> str:
    """根据平台与症状给出性能分析路径。"""

    return diagnose_performance_issue(platform, symptom)
