from django.conf import settings

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.api.serializers import UserSerializer
from authentication.utils import get_current_user


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = get_current_user(request)
        return Response(UserSerializer(instance=user).data, status=status.HTTP_200_OK)


class LoginView(jwt_views.TokenViewBase):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access_token = serializer.validated_data.get("access")
        refresh_token = serializer.validated_data.get("refresh")

        response = Response({"access": access_token}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"],
            value=refresh_token,
            httponly=True,
            path="/api/auth",
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
        )
        return response


class RefreshView(jwt_views.TokenViewBase):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data["refresh"] = self.request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"])
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access_token = serializer.validated_data.get("access")
        refresh_token = serializer.validated_data.get("refresh")

        response = Response({"access": access_token}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"],
            value=refresh_token,
            httponly=True,
            path="/api/auth",
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
        )
        return response


class LogOutView(APIView):
    """Class for logging out a user by clearing tokens."""

    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        refresh_token = self.request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"])
        try:
            token = RefreshToken(refresh_token, verify=False)
            token.blacklist()

            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie(settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"], path="/api/auth")

            return response
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
