import os
import tempfile
import unittest
import uuid

db_file = tempfile.NamedTemporaryFile(delete=False)
db_file.close()
os.environ["DATABASE_URL"] = f"sqlite:///{db_file.name}"

from fastapi.testclient import TestClient
from app.main import app

class BatchUsersTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.admin_username = "admin"
        self.admin_password = "admin123"
        
        self.user1_username = f"user1_{uuid.uuid4().hex}"
        self.user2_username = f"user2_{uuid.uuid4().hex}"
        
        # Register normal test users
        self.client.post("/api/v1/auth/register", json={"username": self.user1_username, "password": "password123"})
        self.client.post("/api/v1/auth/register", json={"username": self.user2_username, "password": "password123"})

    def login(self, username, password):
        response = self.client.post("/api/v1/auth/login", json={"username": username, "password": password})
        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_batch_modify_or_delete(self):
        self.login(self.user1_username, "password123")
        
        # Try batch admin
        res1 = self.client.post("/api/v1/users/batch/admin", json={"user_ids": [1, 2], "is_admin": True})
        self.assertEqual(res1.status_code, 403)
        
        # Try batch delete
        res2 = self.client.post("/api/v1/users/batch/delete", json={"user_ids": [1, 2]})
        self.assertEqual(res2.status_code, 403)

    def test_admin_can_batch_update_admin_status(self):
        self.login(self.admin_username, self.admin_password)
        
        res = self.client.get("/api/v1/users/")
        self.assertEqual(res.status_code, 200)
        users = res.json()
        
        user_ids = [u["id"] for u in users if u["username"] in [self.user1_username, self.user2_username]]
        self.assertEqual(len(user_ids), 2)
        
        # Batch upgrade to admin
        res_upgrade = self.client.post("/api/v1/users/batch/admin", json={"user_ids": user_ids, "is_admin": True})
        self.assertEqual(res_upgrade.status_code, 200)
        
        # Verify status
        res_list = self.client.get("/api/v1/users/")
        users_after = res_list.json()
        for u in users_after:
            if u["id"] in user_ids:
                self.assertTrue(u["is_admin"])

        # Batch downgrade
        res_downgrade = self.client.post("/api/v1/users/batch/admin", json={"user_ids": user_ids, "is_admin": False})
        self.assertEqual(res_downgrade.status_code, 200)
        
        # Verify status
        res_list_2 = self.client.get("/api/v1/users/")
        users_after_2 = res_list_2.json()
        for u in users_after_2:
            if u["id"] in user_ids:
                self.assertFalse(u["is_admin"])

    def test_admin_can_batch_delete_users(self):
        self.login(self.admin_username, self.admin_password)
        
        res = self.client.get("/api/v1/users/")
        users = res.json()
        user_ids = [u["id"] for u in users if u["username"] in [self.user1_username, self.user2_username]]
        
        # Batch delete
        res_del = self.client.post("/api/v1/users/batch/delete", json={"user_ids": user_ids})
        self.assertEqual(res_del.status_code, 200)
        
        # Verify they are gone
        res_list = self.client.get("/api/v1/users/")
        users_after = res_list.json()
        usernames_after = [u["username"] for u in users_after]
        self.assertNotIn(self.user1_username, usernames_after)
        self.assertNotIn(self.user2_username, usernames_after)

    def tearDown(self):
        try:
            os.unlink(db_file.name)
        except OSError:
            pass

if __name__ == "__main__":
    unittest.main()
