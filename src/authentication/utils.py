from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import TokenBackendError
from rest_framework_simplejwt.state import token_backend

from .models import CustomGroup


def get_token(request: Request):
    header = request.META.get(settings.AUTH_HEADER_NAME)
    if header is None:
        raise NotAuthenticated()
    return header.partition("Bearer")[-1].strip()


def get_current_user(request: Request):
    token = get_token(request)
    try:
        payload = token_backend.decode(token, verify=True)
    except TokenBackendError:
        raise TokenBackendError(_("Token is invalid or expired."))

    user_id = payload.get("user_id")

    user_model = get_user_model()
    user = user_model.objects.filter(pk=user_id).first()
    if not user:
        raise NotFound(_(f"User ({user_id}) not found."))
    return user


def is_edit_access_group(user):
    for group in user.groups.all():
        custom_group = CustomGroup.objects.filter(group=group).first()
        if custom_group and custom_group.edit_access:
            return True
    return False
