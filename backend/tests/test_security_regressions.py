import os
import tempfile
import unittest
import uuid

db_file = tempfile.NamedTemporaryFile(delete=False)
db_file.close()
os.environ["DATABASE_URL"] = f"sqlite:///{db_file.name}"

from fastapi.testclient import TestClient

from app.main import app


class SecurityRegressionTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def login(self, username: str, password: str):
        response = self.client.post(
            "/api/v1/auth/login",
            json={"username": username, "password": password},
        )
        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_access_global_config(self):
        username = f"normal_user_config_{uuid.uuid4().hex}"
        self.client.post(
            "/api/v1/auth/register",
            json={"username": username, "password": "pass123"},
        )
        self.login(username, "pass123")

        endpoints = [
            ("/api/v1/config/", "GET", None),
            ("/api/v1/config/models/", "GET", None),
            ("/api/v1/config/tools/", "GET", None),
            ("/api/v1/config/", "PUT", {"kimi_api_key": "sk-test"}),
        ]

        for url, method, body in endpoints:
            response = self.client.request(method, url, json=body)
            self.assertEqual(response.status_code, 403, url)

    def test_conversation_requires_non_empty_model_id(self):
        self.login("admin", "admin123")

        response = self.client.post(
            "/api/v1/assistant/conversations",
            json={"title": "bad", "model_id": ""},
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
