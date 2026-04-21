from __future__ import annotations

import unittest
from dataclasses import dataclass
from unittest.mock import patch

from fastapi.testclient import TestClient

from llm.http.app import create_app


@dataclass
class FakeAnswer:
    summary: str
    architecture_recommendation: str
    performance_recommendation: str
    design_principles: str
    risks: list[str]
    learning_notes: list[str]


class FakeAssistant:
    def ask(self, question: str, context, thread_id: str | None = None) -> FakeAnswer:
        return FakeAnswer(
            summary=f"收到问题: {question}",
            architecture_recommendation=f"平台: {context.target_platform}",
            performance_recommendation="先建立性能基线",
            design_principles="优先遵守单一职责与依赖倒置",
            risks=["抽象过度"],
            learning_notes=["先理解 context_schema", "再理解 structured output"],
        )


class HTTPAppTestCase(unittest.TestCase):
    def test_healthz(self) -> None:
        client = TestClient(create_app())
        response = client.get("/healthz")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_ask_expert(self) -> None:
        with patch("llm.http.app.get_assistant", return_value=FakeAssistant()):
            client = TestClient(create_app())
            response = client.post(
                "/v1/mobile-architect/ask",
                json={
                    "question": "如何设计 Android 架构",
                    "thread_id": "thread-1",
                    "user_name": "Zhuanz",
                    "target_platform": "android",
                    "experience_level": "intermediate",
                    "preferred_language": "java",
                },
            )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["summary"], "收到问题: 如何设计 Android 架构")
        self.assertEqual(body["architecture_recommendation"], "平台: android")
        self.assertEqual(body["risks"], ["抽象过度"])


if __name__ == "__main__":
    unittest.main()
