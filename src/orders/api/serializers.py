from django.conf import settings

from rest_framework.serializers import DateTimeField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from ..constants import ORDER_STATUS
from ..models import Order
from ..models import Post
from ..models import Reason
from ..models import Work
from ..models import WorkCategory


class ReasonSerializer(ModelSerializer):
    class Meta:
        model = Reason
        fields = (
            "pk",
            "name",
            "type",
        )


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "pk",
            "name",
        )


class OrderListSerializer(ModelSerializer):
    date_begin = DateTimeField(**settings.SERIALIZER_DATETIME_PARAMS)
    status_name = SerializerMethodField()
    car_name = SerializerMethodField()
    car_state_number = SerializerMethodField()
    post_name = SerializerMethodField()
    reason_name = SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "pk",
            "number",
            "date_begin",
            "status_name",
            "car_name",
            "car_state_number",
            "post_name",
            "reason_name",
            "note",
        )
        read_only_fields = ("number",)

    def get_status_name(self, obj):
        return dict((x, y) for x, y in ORDER_STATUS).get(obj.status)

    def get_car_name(self, obj):
        return obj.car.name

    def get_car_state_number(self, obj):
        return obj.car.state_number

    def get_post_name(self, obj):
        return obj.post.name

    def get_reason_name(self, obj):
        return obj.reason.name


class OrderDetailSerializer(ModelSerializer):
    created = DateTimeField(**settings.SERIALIZER_DATETIME_PARAMS, read_only=True)
    updated = DateTimeField(**settings.SERIALIZER_DATETIME_PARAMS, read_only=True)
    date_begin = DateTimeField(**settings.SERIALIZER_DATETIME_PARAMS)
    date_end = DateTimeField(**settings.SERIALIZER_DATETIME_PARAMS, required=False, allow_null=True)

    class Meta:
        model = Order
        fields = (
            "pk",
            "created",
            "updated",
            "number",
            "status",
            "reason",
            "date_begin",
            "date_end",
            "post",
            "car",
            "driver",
            "responsible",
            "odometer",
            "note",
        )
        read_only_fields = ("number",)


class WorkCategorySerializer(ModelSerializer):
    class Meta:
        model = WorkCategory
        fields = (
            "pk",
            "name",
        )


class WorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = (
            "pk",
            "category",
            "name",
        )
