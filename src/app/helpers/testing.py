from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class AuthorizationAPITestCase(APITestCase):
    def setUp(self):
        # Create user and token for API
        user_model = get_user_model()
        self.user = user_model.objects.create(username="TestUser", first_name="First", last_name="Last", initials="I")
        self.user_password = "password"
        self.user.set_password(self.user_password)
        self.user.save()
        self.token = AccessToken.for_user(self.user)

        # Set client
        self.client.force_login(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
