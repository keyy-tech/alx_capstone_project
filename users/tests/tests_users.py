from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class UserTests(APITestCase):
    def setUp(self):
        self.url = reverse("register_customer")  # match your urls.py
        self.data = {
            "email": "user@example.com",
            "password": "check@123",
            "first_name": "John",
            "last_name": "Doe",
            "user_profile": {
                "other_name": "Johnny",
                "date_of_birth": "2000-01-01",
                "phone_number": "1234567890",
            },
        }

    def test_create_user(self):
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
