from django.db.models import CharField
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from ..models import Car
from ..models import Employee
from .serializers import CarDetailSerializer
from .serializers import CarShortSerializer
from .serializers import EmployeeDetailSerializer
from .serializers import EmployeeShortSerializer


class CarListView(GenericAPIView):
    """
    Список ТС (без создания, берем из программы Путевки)
    По умолчанию списанные ТС не отображаются

    Filters: show_decommissioned(Bool)
    Search's: state_number_search, name_search
    """

    serializer_class = CarShortSerializer

    def get_queryset(self):
        show_decommissioned = self.request.query_params.get("show_decommissioned")
        if show_decommissioned and show_decommissioned == "True":
            queryset = Car.objects.all()
        else:
            queryset = Car.objects.filter(date_decommissioned=None)

        state_number_search = self.request.query_params.get("state_number_search")
        if state_number_search:
            queryset = queryset.filter(state_number__icontains=state_number_search)

        name_search = self.request.query_params.get("name_search")
        if name_search:
            queryset = queryset.filter(name__icontains=name_search)

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
        return self.partial_update(request, *args, **kwargs)


class EmployeeListView(GenericAPIView):
    """
    Список работников (без создания, берем из программы Путевки)
    По умолчанию уволенные сотрудники не отображаются

    Filters: show_decommissioned(Bool), type
    Search's: fio_search
    """

    serializer_class = EmployeeShortSerializer

    def get_queryset(self):
        show_dismissal = self.request.query_params.get("show_dismissal")
        if show_dismissal and show_dismissal == "True":
            queryset = Employee.objects.all()
        else:
            queryset = Employee.objects.filter(date_dismissal=None)

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
