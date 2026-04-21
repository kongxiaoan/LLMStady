from __future__ import annotations

from langchain.tools import tool


def explain_solid_mapping(problem: str) -> str:
    """把常见问题映射到 SOLID。

    六大设计原则在中文语境里常被表述为：
    单一职责、开闭、里氏替换、接口隔离、依赖倒置、迪米特法则。
    """

    rules = {
        "职责过多": "单一职责原则：一个类只负责一个变化原因。",
        "频繁改老代码": "开闭原则：优先通过扩展新增行为，而不是反复修改稳定代码。",
        "子类行为异常": "里氏替换原则：子类必须可以安全替换父类。",
        "接口臃肿": "接口隔离原则：避免让调用方依赖它不需要的方法。",
        "依赖具体实现": "依赖倒置原则：上层模块依赖抽象，不依赖细节。",
        "调用链过深": "迪米特法则：减少模块间不必要的了解，降低耦合。",
    }

    for keyword, answer in rules.items():
        if keyword in problem:
            return answer

    return (
        "建议从 SOLID 六大设计原则整体检查："
        "职责是否单一、扩展是否容易、继承是否合理、接口是否精简、"
        "依赖是否倒置、模块交互是否过深。"
    )


@tool
def solid_principles_advisor(problem: str) -> str:
    """根据问题描述映射合适的 SOLID / 设计原则建议。"""

    return explain_solid_mapping(problem)
