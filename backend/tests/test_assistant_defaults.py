import unittest

from app.routers.assistant import resolve_knowledge_base_ids, resolve_tool_ids


class AssistantDefaultSelectionTests(unittest.TestCase):
    def test_knowledge_bases_default_to_all(self):
        self.assertEqual(resolve_knowledge_base_ids(None), ["kb_weather", "kb_alert"])
        self.assertEqual(resolve_knowledge_base_ids([]), ["kb_weather", "kb_alert"])

    def test_tools_are_inferred_from_message_when_model_supports_tools(self):
        self.assertEqual(resolve_tool_ids("北京今天的天气怎么样？", True), ["weather_query"])
        self.assertEqual(resolve_tool_ids("广州现在有没有暴雨预警？", True), ["alert_query"])
        self.assertEqual(
            resolve_tool_ids("北京今天的天气和预警情况", True),
            ["weather_query", "alert_query"],
        )

    def test_tools_are_disabled_when_model_does_not_support_tools(self):
        self.assertEqual(resolve_tool_ids("北京今天的天气和预警情况", False), [])


if __name__ == "__main__":
    unittest.main()
