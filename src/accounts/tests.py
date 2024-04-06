from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestAccounts(TestCase):
    def test_create_user(self):
        response = self.client.post(
            "/api/user", {"username": "test_user", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 200)
        try:
            created = User.objects.get(username="test_user")
            self.assertEqual(created.username, "test_user")
            self.assertTrue(created.is_active)
            self.assertFalse(created.is_staff)
        except:
            self.fail()

    def test_delete_user(self):
        User.objects.create_user(username="test_user", password="testpass123")
        response = self.client.delete("/api/user/test_user")
        self.assertEqual(response.status_code, 200)
        try:
            User.objects.get(username="test_user")
            self.fail()
        except:
            pass

    def test_login_action(self):
        User.objects.create_user(username="test_user", password="testpass123")
        response = self.client.post(
            "/api/login", {"username": "test_user", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Redirect"], reverse("posts:posts-page"))
