import os
import unittest
from unittest.mock import patch

from app.config import settings
from app.services.llm import get_llm, get_model_config


class LLMConfigTests(unittest.TestCase):
    def setUp(self):
        self.original_config = settings.get_config_dict(mask_secrets=False)
        self.db_patcher = patch("app.services.llm.SessionLocal")
        self.mock_session_local = self.db_patcher.start()
        self.mock_session_local.return_value.query.return_value.filter.return_value.first.return_value = None

    def tearDown(self):
        self.db_patcher.stop()
        settings.update_config(**self.original_config)

    def test_model_config_uses_latest_runtime_settings(self):
        settings.update_config(
            kimi_api_key="sk-old-kimi",
            deepseek_api_key="sk-old-deepseek",
            minimax_api_key="sk-old-minimax",
            ollama_base_url="http://localhost:11434/v1",
        )

        settings.update_config(
            kimi_api_key="sk-new-kimi",
            deepseek_api_key="sk-new-deepseek",
            minimax_api_key="sk-new-minimax",
            ollama_base_url="http://127.0.0.1:11435/v1",
        )

        self.assertEqual(get_model_config("kimi-k2.5")["api_key"], "sk-new-kimi")
        self.assertEqual(get_model_config("deepseek-v4-flash")["api_key"], "sk-new-deepseek")
        self.assertEqual(get_model_config("MiniMax-M2.5")["api_key"], "sk-new-minimax")
        self.assertEqual(
            get_model_config("deepseek-r1:14b")["base_url"],
            "http://127.0.0.1:11435/v1",
        )

    def test_get_llm_constructs_client_with_latest_runtime_config(self):
        settings.update_config(deepseek_api_key="sk-runtime-deepseek")

        with patch("app.services.llm.ChatOpenAI") as chat_openai:
            llm = get_llm("deepseek-v4-flash", temperature=0.2, streaming=False)

        self.assertIs(llm, chat_openai.return_value)
        chat_openai.assert_called_once_with(
            model="deepseek-v4-flash",
            base_url="https://api.deepseek.com/v1",
            api_key="sk-runtime-deepseek",
            streaming=False,
            temperature=0.2,
        )

    def test_get_llm_passes_optional_timeout_and_retry_config(self):
        settings.update_config(deepseek_api_key="sk-runtime-deepseek")

        with patch("app.services.llm.ChatOpenAI") as chat_openai:
            get_llm(
                "deepseek-v4-flash",
                temperature=0.2,
                streaming=False,
                timeout=12.0,
                max_retries=0,
            )

        chat_openai.assert_called_once_with(
            model="deepseek-v4-flash",
            base_url="https://api.deepseek.com/v1",
            api_key="sk-runtime-deepseek",
            streaming=False,
            temperature=0.2,
            timeout=12.0,
            max_retries=0,
        )

    def test_get_llm_can_disable_environment_proxy(self):
        settings.update_config(deepseek_api_key="sk-runtime-deepseek")

        with patch("app.services.llm.httpx.Client") as http_client:
            with patch("app.services.llm.ChatOpenAI") as chat_openai:
                get_llm(
                    "deepseek-v4-flash",
                    streaming=False,
                    timeout=20.0,
                    use_env_proxy=False,
                )

        http_client.assert_called_once_with(trust_env=False)
        chat_openai.assert_called_once()
        self.assertIs(chat_openai.call_args.kwargs["http_client"], http_client.return_value)

    def test_get_llm_ignores_invalid_ipv6_no_proxy_entry(self):
        settings.update_config(minimax_api_key="sk-runtime-minimax")

        env = {
            "NO_PROXY": "127.0.0.1,localhost,::1,127.0.0.0/8,::1/128",
            "no_proxy": "127.0.0.1,localhost,::1,127.0.0.0/8,::1/128",
        }
        with patch.dict(os.environ, env):
            llm = get_llm("MiniMax-M2.5", streaming=False)

        self.assertEqual(llm.model_name, "MiniMax-M2.5")


if __name__ == "__main__":
    unittest.main()
