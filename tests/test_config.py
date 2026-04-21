from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from llm.config import load_settings


class LoadSettingsTestCase(unittest.TestCase):
    def test_load_settings_reads_app_configuration(self) -> None:
        with patch.dict(
            os.environ,
            {
                "DEEPSEEK_API_KEY": "test-key",
                "DEEPSEEK_BASE_URL": "https://api.deepseek.com",
                "DEEPSEEK_MODEL": "deepseek-chat",
                "APP_TEMPERATURE": "0.2",
                "APP_MAX_RETRIES": "3",
                "APP_DEFAULT_THREAD_ID": "thread-42",
                "APP_DEBUG": "true",
            },
            clear=False,
        ):
            settings = load_settings()

        self.assertEqual(settings.api_key, "test-key")
        self.assertEqual(settings.model, "deepseek-chat")
        self.assertEqual(settings.temperature, 0.2)
        self.assertEqual(settings.max_retries, 3)
        self.assertEqual(settings.default_thread_id, "thread-42")
        self.assertTrue(settings.debug)

    def test_reasoner_is_rejected_for_tool_calling_agent(self) -> None:
        with patch.dict(
            os.environ,
            {
                "DEEPSEEK_API_KEY": "test-key",
                "DEEPSEEK_MODEL": "deepseek-reasoner",
            },
            clear=False,
        ):
            with self.assertRaises(ValueError):
                load_settings()


if __name__ == "__main__":
    unittest.main()
