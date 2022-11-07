from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.helpers.database import get_period_filter_lookup
from app.views import EagerLoadingMixin
from authentication.utils import get_current_user
from orders.constants import COMPLETED

from ..helpers.entrance_general_search import entrance_general_search
from ..helpers.get_provider_list import get_provider_list
from ..helpers.get_queryset_materials_remains import get_queryset_materials_remains
from ..helpers.turnover_moving_material import turnover_moving_material
from ..models import Entrance
from ..models import Material
from ..models import MaterialCategory
from ..models import Turnover
from ..models import Unit
from ..models import Warehouse
from .serializers import EntranceListSerializer
from .serializers import EntranceSerializer
from .serializers import MaterialAvailabilitySerializer
from .serializers import MaterialCategoryListSerializer
from .serializers import MaterialCategorySerializer
from .serializers import MaterialListSerializer
from .serializers import MaterialRemainsCategorySerializer
from .serializers import MaterialRemainsSerializer
from .serializers import MaterialSerializer
from .serializers import TurnoverMaterialReadSerializer
from .serializers import TurnoverMovingMaterialSerializer
from .serializers import TurnoverSerializer
from .serializers import UnitSerializer
from .serializers import WarehouseListSerializer
from .serializers import WarehouseSerializer


class WarehouseListView(CreateModelMixin, GenericAPIView):
    """Список складов"""

    queryset = Warehouse.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WarehouseListSerializer
        return WarehouseSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class WarehouseDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Склад"""

    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.all()

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UnitListView(CreateModelMixin, GenericAPIView):
    """Список единиц измерения"""

    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UnitDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Единица измерения"""

    serializer_class = UnitSerializer
    queryset = Unit.objects.all()

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MaterialCategoryListView(CreateModelMixin, GenericAPIView):
    """Список категорий материалов"""

    queryset = MaterialCategory.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MaterialCategoryListSerializer
        return MaterialCategorySerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MaterialCategoryDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Категория материалов"""

    serializer_class = MaterialCategorySerializer
    queryset = MaterialCategory.objects.all()

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MaterialListView(CreateModelMixin, GenericAPIView):
    """
    Список материалов

    Filters: category(int)
    Search's: general_search
    """

    queryset = Material.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MaterialListSerializer
        return MaterialSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__pk=category)

        general_search = self.request.query_params.get("general_search")
        if general_search:
            queryset = queryset.filter(Q(name__icontains=general_search) | Q(compatbility__icontains=general_search))

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MaterialDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    Материал

    availability_mode - short serializer with warehouses availability
    """

    queryset = Material.objects.all()

    def get_serializer_class(self):
        availability_mode = self.request.query_params.get("availability_mode")
        if availability_mode and availability_mode == "true":
            return MaterialAvailabilitySerializer
        return MaterialSerializer

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EntranceListView(EagerLoadingMixin, ListAPIView, CreateModelMixin):
    """
    Список поступлений

    Filters: date_begin(date_str), date_end(date_str)
    Search's: general_search (provider, document_number, turnovers_from_entrance__material__name)
    """

    queryset = Entrance.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EntranceListSerializer
        return EntranceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")
        if date_begin or date_end:
            queryset = queryset.filter(get_period_filter_lookup("date", date_begin, date_end))

        general_search = self.request.query_params.get("general_search")
        if general_search:
            queryset = entrance_general_search(queryset, str(general_search))

        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EntranceDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Поступление"""

    serializer_class = EntranceSerializer
    queryset = Entrance.objects.all()

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProviderListView(APIView):
    """ "Список поставщиков"""

    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response(get_provider_list())


class TurnoverListView(GenericAPIView, CreateModelMixin):
    """
    Обороты
    Filters: order_pk(int) or entrance_pk(int)
    """

    serializer_class = TurnoverSerializer

    def get_queryset(self):
        queryset = Turnover.objects.none()

        order_pk = self.request.query_params.get("order_pk")
        entrance_pk = self.request.query_params.get("entrance_pk")

        if order_pk:
            queryset = Turnover.objects.filter(order__pk=order_pk)
        elif entrance_pk:
            queryset = Turnover.objects.filter(entrance__pk=entrance_pk)

        queryset = queryset.order_by("pk")

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TurnoverMaterialListView(EagerLoadingMixin, ListAPIView):
    """
    Обороты по материалу

    Filters: type
    """

    serializer_class = TurnoverMaterialReadSerializer

    def get_queryset(self):
        queryset = Turnover.objects.none()

        material_pk = self.request.query_params.get("material_pk")
        if material_pk:
            queryset = Turnover.objects.filter(material__pk=material_pk)

        warehouse = self.request.query_params.get("warehouse")
        if warehouse:
            queryset = queryset.filter(warehouse=warehouse)

        turnover_type = self.request.query_params.get("turnover_type")
        if turnover_type:
            if warehouse:
                queryset = queryset.filter(type=turnover_type)
            else:
                queryset = queryset.filter(type=turnover_type, is_correction=False)

        sort_field = self.request.query_params.get("sortField")
        sort_order = self.request.query_params.get("sortOrder")
        if sort_field and sort_order:
            sort_order = "-" if sort_order == "descend" else ""
            queryset = queryset.order_by(f"{sort_order}{sort_field}", f"{sort_order}pk")
        else:
            queryset = queryset.order_by("-date", "-pk")

        return queryset


class TurnoverDetailView(RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """Оборот"""

    serializer_class = TurnoverSerializer
    queryset = Turnover.objects.all()

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()

        user = get_current_user(request)

        if (obj.order and obj.order.status != COMPLETED) or user.is_superuser:
            self.perform_destroy(obj)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            data={"message": "Обороты удалять запрещено, разрешено только из незавершенных заказ-нарядов"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class MaterialRemainsListView(EagerLoadingMixin, ListAPIView):
    """
    Список материалов с остатком

    Filters: category(list(int)), warehouses(int), compatbility(list(str)), hide_empty(bool), compatbility_show_empty(bool)
    Search's: search_name
    """

    serializer_class = MaterialRemainsSerializer
    queryset = Material.objects.none()

    def get_queryset(self):
        category = self.request.query_params.get("category")
        warehouse = self.request.query_params.get("warehouse")
        compatbility = self.request.query_params.get("compatbility")
        hide_empty = self.request.query_params.get("hide_empty")
        search_name = self.request.query_params.get("search_name")

        queryset = get_queryset_materials_remains(category, warehouse, compatbility, hide_empty, search_name, False)

        sort_field = self.request.query_params.get("sortField")
        sort_order = self.request.query_params.get("sortOrder")

        if sort_field and sort_order:
            sort_order = "-" if sort_order == "descend" else ""

            if sort_field == "category_name":
                sort_field = "category__name"

            queryset = queryset.order_by(f"{sort_order}{sort_field}", "pk")
        else:
            queryset.order_by("name")

        return queryset


class MaterialRemainsCategoryListView(EagerLoadingMixin, ListAPIView):
    """
    Список материалов с остатком по категориям

    Filters: category(list(int)), warehouses(int), compatbility(list(str)), hide_empty(bool), compatbility_show_empty(bool)
    Search's: search_name
    """

    serializer_class = MaterialRemainsCategorySerializer
    queryset = Material.objects.none()

    def get_queryset(self):
        category = self.request.query_params.get("category")
        warehouse = self.request.query_params.get("warehouse")
        compatbility = self.request.query_params.get("compatbility")
        search_name = self.request.query_params.get("search_name")

        queryset = get_queryset_materials_remains(category, warehouse, compatbility, "true", search_name, True)

        sort_field = self.request.query_params.get("sortField")
        sort_order = self.request.query_params.get("sortOrder")

        if sort_field and sort_order:
            sort_order = "-" if sort_order == "descend" else ""

            if sort_field == "category_name":
                sort_field = "category__name"

            queryset = queryset.order_by(f"{sort_order}{sort_field}", "pk")
        else:
            queryset.order_by("name")

        return queryset

    def get(self, request, *args, **kwargs):
        category = self.request.query_params.get("category")
        search_name = self.request.query_params.get("search_name")
        if not category and not search_name:
            return Response(
                data={"message": "category - обязательный параметр"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TurnoverMovingMaterialView(GenericAPIView):
    serializer_class = TurnoverMovingMaterialSerializer
    queryset = Turnover.objects.none()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_current_user(request)

        try:
            turnover_moving_material(serializer.data, user)
            return Response(data={"message": "Успешно перемещено"}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(data={"message": "Ошибка при перемещении"}, status=status.HTTP_400_BAD_REQUEST)
