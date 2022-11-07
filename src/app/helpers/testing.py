import json
from decimal import Decimal

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


def get_test_user():
    user_model = get_user_model()

    username = "TestUser"
    user = user_model.objects.filter(username=username).first()
    if user is None:
        user = user_model.objects.create(username="TestUser", first_name="First", last_name="Last", initials="I")

    return user


class AuthorizationAPITestCase(APITestCase):
    def setUp(self):
        # Create user and token for API
        self.user = get_test_user()
        self.user_password = "password"
        self.user.set_password(self.user_password)
        self.user.save()
        self.token = AccessToken.for_user(self.user)

        # Set client
        self.client.force_login(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
