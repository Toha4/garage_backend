from http.cookies import SimpleCookie

from django.conf import settings
from django.urls import reverse

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from app.helpers.testing import LoginAPITestCase
from authentication.api.serializers import UserSerializer


class UserApiTestCase(LoginAPITestCase):
    def test_login(self):
        url = reverse("token-obtain")
        response = self.client.post(url, {"username": self.user.username, "password": self.user_password})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue("access" in response.data.keys())

    def test_refresh(self):
        refresh_token = RefreshToken.for_user(self.user)
        self.client.cookies = SimpleCookie({settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"]: refresh_token})

        url = reverse("token-refresh")
        response = self.client.post(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue("access" in response.data.keys())

    def test_logout(self):
        refresh_token = RefreshToken.for_user(self.user)
        self.client.cookies = SimpleCookie({settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"]: refresh_token})

        url = reverse("logout")
        response = self.client.post(url)

        self.assertEqual(status.HTTP_205_RESET_CONTENT, response.status_code)

    def test_get_me(self):
        url = reverse("user-detail")
        response = self.client.get(url)

        serializer_data = UserSerializer(self.user).data

        self.assertEqual(serializer_data, response.data)
