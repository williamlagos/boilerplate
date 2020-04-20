from django.test import TestCase
from rest_framework.test import APIClient

# Create your tests here.

class HealthTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()

    def test_health_endpoint(self):
        response = self.c.get('/health')
        assert response.status_code == 301, \
            "Expect 301 Permanently moved. got: {}" . format (response.status_code)