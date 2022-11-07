from django.conf import settings

from rest_framework.serializers import DateField
from rest_framework.serializers import DecimalField
from rest_framework.serializers import Field
from rest_framework.serializers import HiddenField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework.serializers import SerializerMethodField

from app.helpers.serializers import CurrentUserDefault

from ..constants import COMING
from ..helpers.material_utils import get_material_in_warehouses
from ..helpers.material_utils import get_material_prices
from ..helpers.material_utils import get_material_remains
from ..models import Entrance
from ..models import Material
from ..models import MaterialCategory
from ..models import Turnover
from ..models import Unit
from ..models import Warehouse


class PositiveExpensesTurnoverSerializerField(Field):
    def to_representation(self, obj):
        return abs(obj)

    def to_internal_value(self, data):
        return data


class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = (
            "pk",
            "name",
        )


class WarehouseListSerializer(WarehouseSerializer):
    delete_forbidden = SerializerMethodField()

    class Meta(WarehouseSerializer.Meta):
        fields = WarehouseSerializer.Meta.fields + ("delete_forbidden",)

    def get_delete_forbidden(self, obj):
        return obj.turnovers.all().exists()


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = (
            "pk",
            "name",
            "is_precision_point",
        )


class MaterialCategorySerializer(ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = (
            "pk",
            "name",
        )


class MaterialCategoryListSerializer(MaterialCategorySerializer):
    material_count = SerializerMethodField()

    class Meta(MaterialCategorySerializer.Meta):
        fields = MaterialCategorySerializer.Meta.fields + ("material_count",)

    def get_material_count(self, obj):
        return Material.objects.filter(category=obj).count()


class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Material
        fields = (
            "pk",
            "name",
            "unit",
            "category",
            "article_number",
            "compatbility",
        )


class MaterialListSerializer(MaterialSerializer):
    delete_forbidden = SerializerMethodField()
    unit_name = SerializerMethodField()
    unit_is_precision_point = SerializerMethodField()

    class Meta(MaterialSerializer.Meta):
        fields = MaterialSerializer.Meta.fields + (
            "delete_forbidden",
            "unit_name",
            "unit_is_precision_point",
        )

    def get_delete_forbidden(self, obj):
        return obj.turnovers.all().exists()

    def get_unit_name(self, obj):
        if obj.unit:
            return obj.unit.name
        return None

    def get_unit_is_precision_point(self, obj):
        if obj.unit:
            return obj.unit.is_precision_point
        return None


class MaterialAvailabilitySerializer(ModelSerializer):
    warehouses_availability = SerializerMethodField()
    prices = SerializerMethodField()
    quantity = SerializerMethodField()
    unit_name = SerializerMethodField()
    unit_is_precision_point = SerializerMethodField()

    class Meta:
        model = Material
        fields = (
            "pk",
            "name",
            "warehouses_availability",
            "prices",
            "quantity",
            "unit_name",
            "unit_is_precision_point",
        )

    def get_warehouses_availability(self, obj):
        return get_material_in_warehouses(obj.pk)

    def get_prices(self, obj):
        return get_material_prices(obj.pk)

    def get_quantity(self, obj):
        return get_material_remains(obj.pk)

    def get_unit_name(self, obj):
        if obj.unit:
            return obj.unit.name
        return None

    def get_unit_is_precision_point(self, obj):
        if obj.unit:
            return obj.unit.is_precision_point
        return None


class TurnoverSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    date = DateField(**settings.SERIALIZER_DATE_PARAMS)
    material_name = SerializerMethodField()
    warehouse_name = SerializerMethodField()
    material_unit_name = SerializerMethodField()
    material_unit_is_precision_point = SerializerMethodField()
    price = DecimalField(max_digits=12, decimal_places=2, coerce_to_string=False)
    quantity = DecimalField(max_digits=9, decimal_places=2, coerce_to_string=False)
    sum = DecimalField(max_digits=12, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Turnover
        fields = (
            "pk",
            "type",
            "date",
            "is_correction",
            "note",
            "user",
            "material",
            "material_name",
            "material_unit_name",
            "material_unit_is_precision_point",
            "warehouse",
            "warehouse_name",
            "price",
            "quantity",
            "sum",
            "order",
            "entrance",
        )

    def get_material_name(self, obj):
        if obj.material:
            return obj.material.name
        return ""

    def get_warehouse_name(self, obj):
        if obj.warehouse:
            return obj.warehouse.name
        return ""

    def get_material_unit_name(self, obj):
        if obj.material:
            return obj.material.unit.name
        return None

    def get_material_unit_is_precision_point(self, obj):
        if obj.material:
            return obj.material.unit.is_precision_point
        return None


class TurnoverNestedWriteSerializer(TurnoverSerializer):
    class Meta(TurnoverSerializer.Meta):
        extra_kwargs = {
            "pk": {"read_only": False, "required": False, "allow_null": True},
        }


class TurnoverOrderNestedWriteSerializer(TurnoverNestedWriteSerializer):
    quantity = PositiveExpensesTurnoverSerializerField()
    sum = PositiveExpensesTurnoverSerializerField()


class TurnoverMaterialReadSerializer(ModelSerializer):
    date = DateField(**settings.SERIALIZER_DATE_PARAMS)
    user_name = SerializerMethodField()
    turnover_name = SerializerMethodField()
    warehouse_name = SerializerMethodField()
    quantity_with_unit = SerializerMethodField()
    quantity = DecimalField(max_digits=9, decimal_places=2, coerce_to_string=False)
    price = DecimalField(max_digits=12, decimal_places=2, coerce_to_string=False)
    sum = DecimalField(max_digits=12, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Turnover
        fields = (
            "pk",
            "type",
            "date",
            "is_correction",
            "user_name",
            "turnover_name",
            "warehouse_name",
            "quantity",
            "quantity_with_unit",
            "price",
            "sum",
            "order",
            "entrance",
        )

    def get_user_name(self, obj):
        if obj.user:
            return f"{obj.user.last_name} {obj.user.first_name[:1]} {obj.user.initials}"
        return ""

    def get_turnover_name(self, obj):
        if obj.is_correction:
            return f"Корректировка ({obj.note})"
        elif obj.order:
            return f"Списание заказ-наряд №{obj.order.number} ({obj.order.car.state_number})"
        elif obj.entrance:
            provider = f"от {obj.entrance.provider}" if obj.entrance.provider else ""
            document_number = f" (№ документа {obj.entrance.document_number})" if obj.entrance.document_number else ""
            return f"Приход {provider}{document_number}"

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    def get_quantity_with_unit(self, obj):
        return f"{round(obj.quantity, 2 if obj.material.unit.is_precision_point else 0)} {obj.material.unit.name}"


class TurnoverMovingMaterialSerializer(Serializer):
    material = IntegerField()
    date = DateField(**settings.SERIALIZER_DATE_PARAMS)
    warehouse_outgoing = IntegerField()
    warehouse_incoming = IntegerField()
    quantity = DecimalField(max_digits=18, decimal_places=2, coerce_to_string=False)
    price = DecimalField(max_digits=18, decimal_places=2, coerce_to_string=False)
    sum = DecimalField(max_digits=18, decimal_places=2, coerce_to_string=False)


class EntranceListSerializer(ModelSerializer):
    date = DateField(**settings.SERIALIZER_DATE_PARAMS)

    class Meta:
        model = Entrance
        fields = (
            "pk",
            "date",
            "document_number",
            "provider",
            "note",
        )


class EntranceSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    date = DateField(**settings.SERIALIZER_DATE_PARAMS)
    turnovers_from_entrance = TurnoverNestedWriteSerializer(many=True)

    class Meta:
        model = Entrance
        fields = (
            "pk",
            "user",
            "date",
            "document_number",
            "responsible",
            "provider",
            "note",
            "turnovers_from_entrance",
        )

    def run_validation(self, data):
        for turnover_material in data["turnovers_from_entrance"]:
            turnover_material["type"] = COMING

        validated_data = super().run_validation(data=data)
        return validated_data

    def create(self, validated_data):
        turnovers_from_entrance = validated_data.pop("turnovers_from_entrance")

        entrance = self.Meta.model.objects.create(**validated_data)

        for turnover_material in turnovers_from_entrance:
            turnover_material["date"] = entrance.date
            turnover_material["user"] = entrance.user
            entrance.turnovers_from_entrance.create(**turnover_material)

        return entrance

    def update(self, instance, validated_data):
        turnovers_from_entrance = validated_data.pop("turnovers_from_entrance")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Сохраняем только вновь добавленные материалы
        for turnover_material in turnovers_from_entrance:
            if "pk" not in turnover_material or turnover_material["pk"] is None:
                turnover_material["date"] = instance.date
                turnover_material["user"] = instance.user
                instance.turnovers_from_entrance.create(**turnover_material)

        return instance


class MaterialRemainsSerializer(ModelSerializer):
    pk = SerializerMethodField()
    name = SerializerMethodField()
    category = SerializerMethodField()
    category_name = SerializerMethodField()
    unit_name = SerializerMethodField()
    unit_is_precision_point = SerializerMethodField()
    warehouses_availability = SerializerMethodField()
    compatbility = SerializerMethodField()
    quantity = SerializerMethodField()
    price = SerializerMethodField()
    sum = SerializerMethodField()

    class Meta:
        model = Material
        fields = (
            "pk",
            "name",
            "category",
            "category_name",
            "unit_name",
            "unit_is_precision_point",
            "compatbility",
            "warehouses_availability",
            "quantity",
            "price",
            "sum",
        )

    def get_pk(self, obj):
        return obj["pk"]

    def get_name(self, obj):
        return obj["name"]

    def get_category(self, obj):
        return obj["category"]

    def get_category_name(self, obj):
        return obj["category__name"]

    def get_unit_name(self, obj):
        return obj["unit__name"]

    def get_unit_is_precision_point(self, obj):
        return obj["unit__is_precision_point"]

    def get_compatbility(self, obj):
        return obj["compatbility"]

    def get_warehouses_availability(self, obj):
        if obj["quantity"] and obj["quantity"] > 0.00:
            return get_material_in_warehouses(obj["pk"], True)
        return []

    def get_quantity(self, obj):
        if obj["quantity"]:
            return obj["quantity"]
        return 0.00

    def get_price(self, obj):
        if obj["quantity"] and obj["sum"]:
            return round(obj["sum"] / obj["quantity"], 2)
        return 0.00

    def get_sum(self, obj):
        if obj["sum"]:
            return obj["sum"]
        return 0.00


class MaterialRemainsCategorySerializer(ModelSerializer):
    pk = SerializerMethodField()
    name = SerializerMethodField()
    category = SerializerMethodField()
    unit_name = SerializerMethodField()
    unit_is_precision_point = SerializerMethodField()
    compatbility = SerializerMethodField()
    warehouse = SerializerMethodField()
    warehouse_name = SerializerMethodField()
    quantity = SerializerMethodField()
    price = SerializerMethodField()
    sum = SerializerMethodField()

    class Meta:
        model = Material
        fields = (
            "pk",
            "name",
            "category",
            "unit_name",
            "unit_is_precision_point",
            "warehouse",
            "warehouse_name",
            "compatbility",
            "quantity",
            "price",
            "sum",
        )

    def get_pk(self, obj):
        return obj["pk"]

    def get_name(self, obj):
        return obj["name"]

    def get_category(self, obj):
        return obj["category"]

    def get_unit_name(self, obj):
        return obj["unit__name"]

    def get_unit_is_precision_point(self, obj):
        return obj["unit__is_precision_point"]

    def get_warehouse(self, obj):
        return obj["turnovers__warehouse"]

    def get_warehouse_name(self, obj):
        return obj["turnovers__warehouse__name"]

    def get_compatbility(self, obj):
        return obj["compatbility"]

    def get_quantity(self, obj):
        if obj["quantity"]:
            return obj["quantity"]
        return 0.00

    def get_price(self, obj):
        if obj["quantity"] and obj["sum"]:
            return round(obj["sum"] / obj["quantity"], 2)
        return 0.00

    def get_sum(self, obj):
        if obj["sum"]:
            return obj["sum"]
        return 0.00
