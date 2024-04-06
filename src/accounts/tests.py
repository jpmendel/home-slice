from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestUserManagement(TestCase):
    def test_create_user_success(self):
        response = self.client.post(
            "/api/user", {"username": "test_user", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 200)
        try:
            created = User.objects.get(username="test_user")
        except:
            self.fail()
        self.assertEqual(created.username, "test_user")
        self.assertFalse(created.is_staff)

    def test_create_admin_success(self):
        response = self.client.post(
            "/api/user",
            {"username": "test_admin", "password": "testpass123", "isAdmin": True},
        )
        self.assertEqual(response.status_code, 200)
        try:
            created = User.objects.get(username="test_admin")
        except:
            self.fail()
        self.assertEqual(created.username, "test_admin")
        self.assertTrue(created.is_staff)

    def test_create_user_missing_info(self):
        response = self.client.post("/api/user", {"username": "test_user"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"), "Username and password required"
        )
        # Check that nothing was created
        try:
            User.objects.get(username="test_user")
            self.fail()
        except:
            pass

    def test_create_user_already_exists(self):
        User.objects.create_user(username="test_user", password="testpass123")
        response = self.client.post(
            "/api/user", {"username": "test_user", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"),
            'User with name "test_user" already exists',
        )

    def test_delete_user_success(self):
        User.objects.create_user(username="test_user", password="testpass123")
        response = self.client.delete("/api/user/test_user")
        self.assertEqual(response.status_code, 200)
        try:
            User.objects.get(username="test_user")
            self.fail()
        except:
            pass

    def test_delete_user_missing_info(self):
        User.objects.create_user(username="test_user", password="testpass123")
        response = self.client.delete("/api/user")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"), "Username must be provided to delete"
        )
        # Check that nothing was deleted
        try:
            User.objects.get(username="test_user")
        except:
            self.fail()

    def test_delete_user_not_found(self):
        User.objects.create_user(username="test_user", password="testpass123")
        response = self.client.delete("/api/user/other_user")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.content.decode("utf-8"),
            'User with username "other_user" not found',
        )
        # Check that nothing was deleted
        try:
            User.objects.get(username="test_user")
        except:
            self.fail()


class TestLoginLogout(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="testpass123")

    def test_login_success(self):
        response = self.client.post(
            "/api/login", {"username": "test_user", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Redirect"], reverse("posts:page-posts"))

    def test_login_empty(self):
        response = self.client.post("/api/login", {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"), "Invalid username or password"
        )

    def test_login_invalid_username(self):
        response = self.client.post(
            "/api/login", {"username": "other_user", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"), "Invalid username or password"
        )

    def test_login_invalid_password(self):
        response = self.client.post(
            "/api/login", {"username": "test_user", "password": "wrongpass123"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"), "Invalid username or password"
        )
