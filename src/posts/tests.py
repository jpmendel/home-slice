from urllib.parse import urlencode
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post


class TestPostManagement(TestCase):
    author: User

    def setUp(self):
        self.author = User.objects.create_user(
            username="test_user", password="testpass123"
        )
        Post.objects.create(author=self.author, content="My first post")
        Post.objects.create(author=self.author, content="My second post")
        Post.objects.create(author=self.author, content="My third post")
        is_success = self.client.login(username="test_user", password="testpass123")
        if not is_success:
            self.fail()

    def test_get_posts_all_success(self):
        response = self.client.get("/api/post")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="My first post")
        self.assertContains(response, text="My second post")
        self.assertContains(response, text="My third post")

    def test_get_posts_all_empty(self):
        for post in Post.objects.all():
            post.delete()
        response = self.client.get("/api/post")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, text="My first post")
        self.assertNotContains(response, text="My second post")
        self.assertNotContains(response, text="My third post")

    def test_get_posts_one_success(self):
        response = self.client.get("/api/post/2")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, text="My first post")
        self.assertContains(response, text="My second post")
        self.assertNotContains(response, text="My third post")

    def test_get_posts_one_not_found(self):
        response = self.client.get("/api/post/4")
        self.assertEqual(response.status_code, 404)

    def test_create_post_success(self):
        response = self.client.post("/api/post", {"content": "My fourth post"})
        self.assertEqual(response.status_code, 200)
        try:
            created = Post.objects.get(id=4)
        except:
            self.fail()
        self.assertEqual(created.content, "My fourth post")

    def test_update_post_success(self):
        response = self.client.put(
            "/api/post/3", urlencode({"content": "My updated third post"})
        )
        self.assertEqual(response.status_code, 200)
        try:
            updated = Post.objects.get(id=3)
        except:
            self.fail()
        self.assertEqual(updated.content, "My updated third post")
        self.assertNotEqual(updated.updated_at, None)

    def test_update_post_not_found(self):
        response = self.client.put(
            "/api/post/4", urlencode({"content": "My updated fourth post"})
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_post_success(self):
        response = self.client.delete("/api/post/1")
        self.assertEqual(response.status_code, 200)
        try:
            Post.objects.get(id=1)
            self.fail()
        except:
            pass

    def test_delete_post_not_found(self):
        response = self.client.delete("/api/post/4")
        self.assertEqual(response.status_code, 404)
