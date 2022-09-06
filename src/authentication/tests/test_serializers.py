from django.contrib.auth import get_user_model
from django.test import TestCase

from authentication.api.serializers import UserSerializer


class UserSerializerTestCase(TestCase):
    def test_ok(self):
        user_model = get_user_model()
        user = user_model.objects.create(
            username="TestUser", first_name="First", last_name="Last", initials="I", is_superuser=False
        )
        data = UserSerializer(user).data
        expected_data = {
            "pk": user.pk,
            "first_name": "First",
            "last_name": "Last",
            "full_name": "First Last",
            "initials": "I",
            "is_superuser": False,
            "edit_access": False,
        }
        self.assertEqual(expected_data, data)
