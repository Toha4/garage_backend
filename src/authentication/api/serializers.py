from rest_framework import serializers

from authentication.utils import is_edit_access_group

from ..models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    edit_access = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "pk",
            "first_name",
            "last_name",
            "full_name",
            "initials",
            "is_superuser",
            "edit_access",
        )

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_edit_access(self, obj):
        if obj.is_superuser or is_edit_access_group(obj):
            return True
        return False
