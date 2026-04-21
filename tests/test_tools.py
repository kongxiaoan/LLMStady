from __future__ import annotations

import unittest

from llm.tools.architecture import generate_architecture_advice
from llm.tools.performance import diagnose_performance_issue
from llm.tools.principles import explain_solid_mapping
from llm.tools.review import build_review_checklist


class MobileExpertToolsTestCase(unittest.TestCase):
    def test_architecture_advice_contains_android_guidance(self) -> None:
        result = generate_architecture_advice("android", "super-app", "large")
        self.assertIn("Clean Architecture", result)
        self.assertIn("插件化", result)

    def test_performance_tool_highlights_startup_path(self) -> None:
        result = diagnose_performance_issue("android", "启动慢")
        self.assertIn("Application 初始化", result)

    def test_principles_tool_maps_problem_to_solid(self) -> None:
        result = explain_solid_mapping("这个类职责过多，而且后续维护很难")
        self.assertIn("单一职责原则", result)

    def test_review_checklist_contains_focus_items(self) -> None:
        result = build_review_checklist("ios", "性能与架构")
        self.assertIn("主线程阻塞", result)
        self.assertIn("稳定抽象层", result)


if __name__ == "__main__":
    unittest.main()
