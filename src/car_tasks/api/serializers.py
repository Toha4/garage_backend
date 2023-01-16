from django.conf import settings

from rest_framework.serializers import DateField
from rest_framework.serializers import HiddenField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import ValidationError

from app.helpers.database import convert_to_localtime
from app.helpers.serializers import CurrentUserDefault

from ..models import CarTask


class CarTaskSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    created = SerializerMethodField()
    date_completed = DateField(**settings.SERIALIZER_DATE_PARAMS, required=False, allow_null=True)

    class Meta:
        model = CarTask
        fields = (
            "pk",
            "user",
            "created",
            "car",
            "description",
            "materials",
            "is_completed",
            "date_completed",
            "order",
        )

    def get_created(self, obj):
        if obj.created:
            return convert_to_localtime(obj.created).strftime("%d.%m.%Y")
        return ""

    def validate(self, data):
        if data.get("is_completed") and data.get("date_completed") is None:
            raise ValidationError({"error": ('"date_completed" обязательное поле если "is_completed" == True ')})
        return data


class CarTaskListSerializer(CarTaskSerializer):
    car_name = SerializerMethodField()
    order_number = SerializerMethodField()

    class Meta(CarTaskSerializer.Meta):
        fields = CarTaskSerializer.Meta.fields + (
            "car_name",
            "order_number",
        )

    def get_car_name(self, obj):
        return f"{obj.car.state_number} - {obj.car.name}"

    def get_order_number(self, obj):
        if obj.order:
            return obj.order.number
        return None
