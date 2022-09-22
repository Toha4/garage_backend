from django.conf import settings
from django.utils.translation import gettext_lazy as _

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.serializers import DateTimeField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from ..constants import ORDER_STATUS
from ..helpers.validators_order import validator_mechanics_order_work
from ..helpers.validators_order import validator_order_works
from ..models import Order
from ..models import OrderWork
from ..models import OrderWorkMechanic
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


class OrderWorkMechanickSerializer(ModelSerializer):
    class Meta:
        model = OrderWorkMechanic
        fields = (
            "pk",
            "mechanic",
            "time_minutes",
        )


class OrderWorkSerializer(WritableNestedModelSerializer):
    mechanics = OrderWorkMechanickSerializer(many=True)

    class Meta:
        model = OrderWork
        fields = (
            "pk",
            "work",
            "quantity",
            "time_minutes",
            "note",
            "mechanics",
        )


class OrderDetailSerializer(WritableNestedModelSerializer):
    created = DateTimeField(**settings.SERIALIZER_DATETIME_PARAMS, read_only=True)
    updated = DateTimeField(**settings.SERIALIZER_DATETIME_PARAMS, read_only=True)
    date_begin = DateTimeField(**settings.SERIALIZER_DATETIME_PARAMS)
    date_end = DateTimeField(**settings.SERIALIZER_DATETIME_PARAMS, required=False, allow_null=True)
    order_works = OrderWorkSerializer(many=True)

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
            "order_works",
        )
        read_only_fields = ("number",)

    def validate(self, data):
        order_works = data.get("order_works")
        if order_works:
            validator_order_works(order_works)

            for order_work in order_works:
                mechanics = order_work.get("mechanics")
                if mechanics:
                    validator_mechanics_order_work(mechanics, order_work.get("work").pk)

        return data


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
