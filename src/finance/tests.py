from django.test import TestCase
from django.contrib.auth.models import User


class TestStockPricePlot(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="testpass123")
        is_success = self.client.login(username="test_user", password="testpass123")
        if not is_success:
            self.fail()

    def test_get_stocks_success(self):
        response = self.client.get("/api/stocks/STOCK")
        self.assertEqual(response.status_code, 200)
