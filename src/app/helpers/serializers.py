from authentication.utils import get_current_user


class CurrentUserDefault(object):   
    requires_context = True

    def __call__(self, serializer_field):
        request = serializer_field.context["request"]
        user = get_current_user(request)
        return user