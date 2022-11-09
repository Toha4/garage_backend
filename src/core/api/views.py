from datetime import datetime

from django.db.models import CharField
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from warehouse.helpers.update_car_tag_material import update_car_tag_material

from ..models import Car
from ..models import Employee
from .serializers import CarDetailSerializer
from .serializers import CarShortSerializer
from .serializers import CarTagSerializer
from .serializers import EmployeeDetailSerializer
from .serializers import EmployeeShortSerializer


class CarListView(GenericAPIView):
    """
    Список ТС (без создания, берем из программы Путевки)
    По умолчанию списанные ТС не отображаются

    Filters: show_decommissioned(Bool)
    Search's: state_number_search, name_search, general_search(state_number, name)
    """

    serializer_class = CarShortSerializer

    def get_queryset(self):
        queryset = Car.objects.all()

        date_request = self.request.query_params.get("date_request")
        show_decommissioned = self.request.query_params.get("show_decommissioned")
        if date_request:
            queryset = queryset.filter(
                Q(date_decommissioned=None) | Q(date_decommissioned__gte=datetime.strptime(date_request, "%d.%m.%Y"))
            )
        elif show_decommissioned is None or show_decommissioned == "False":
            queryset = queryset.filter(date_decommissioned=None)

        state_number_search = self.request.query_params.get("state_number_search")
        if state_number_search:
            queryset = queryset.filter(state_number__icontains=state_number_search)

        name_search = self.request.query_params.get("name_search")
        if name_search:
            queryset = queryset.filter(name__icontains=name_search)

        general_search = self.request.query_params.get("general_search")
        if general_search:
            queryset = queryset.filter(Q(name__icontains=general_search) | Q(state_number__icontains=general_search))

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CarDetailView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    """ТС (без удаления, изменить можно только поле - name)"""

    serializer_class = CarDetailSerializer
    queryset = Car.objects.all()

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        car = get_object_or_404(self.queryset, pk=pk)
        old_name = car.name

        updated_car = self.partial_update(request, *args, **kwargs)

        change_tags_in_material = self.request.query_params.get("change_tags_in_material")
        if change_tags_in_material == "true":
            name = updated_car.data.get("name")
            update_car_tag_material(old_name, name)
            
        return updated_car


class CarTagsListView(GenericAPIView):
    serializer_class = CarTagSerializer
    queryset = Car.objects.all().distinct("name")

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeListView(GenericAPIView):
    """
    Список работников (без создания, берем из программы Путевки)
    По умолчанию уволенные сотрудники не отображаются

    Filters: show_dismissal(Bool), type
    Search's: fio_search
    """

    serializer_class = EmployeeShortSerializer

    def get_queryset(self):
        queryset = Employee.objects.all()

        date_request = self.request.query_params.get("date_request")
        show_dismissal = self.request.query_params.get("show_dismissal")
        if date_request:
            queryset = queryset.filter(
                Q(date_dismissal=None) | Q(date_dismissal__gte=datetime.strptime(date_request, "%d.%m.%Y"))
            )
        elif show_dismissal is None or show_dismissal == "False":
            queryset = queryset.filter(date_dismissal=None)

        type_ = self.request.query_params.get("type")
        if type_:
            queryset = queryset.filter(type=type_)

        fio_search = self.request.query_params.get("fio_search")
        if fio_search:
            queryset = queryset.annotate(
                fio=Concat("first_name", V(" "), "last_name", V(" "), "patronymic", output_filed=CharField())
            ).filter(fio__icontains=fio_search)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeDetailView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    """Работник (без удаления, изменить можно только поле - type)"""

    serializer_class = EmployeeDetailSerializer
    queryset = Employee.objects.all()

    def get_object(self):
        pk = self.kwargs.pop("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
