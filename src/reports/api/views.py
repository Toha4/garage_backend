from django.db.models import CharField
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from app.views import EagerLoadingMixin
from core.models import Car
from core.models import Employee

from ..helpers.get_report_cars_queryset import get_report_cars_queryset
from ..helpers.get_report_materials_queryset import get_report_materials_queryset
from ..helpers.get_report_mechanics_queryset import get_report_mechanics_queryset
from ..models import EmployeeNote
from ..reports.report_cars_excel import report_cars_excel
from ..reports.report_materials_excel import report_materials_excel
from ..reports.report_mechanics_excel import report_mechanics_excel
from .serializers import EmployeeNoteSerializer
from .serializers import ReportCarSerializer
from .serializers import ReportMaterialSerializer
from .serializers import ReportMechanicsSerializer


class EmployeeNoteListView(EagerLoadingMixin, ListAPIView, CreateModelMixin):
    """Список записей по работникам"""

    serializer_class = EmployeeNoteSerializer
    queryset = EmployeeNote.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        general_search = self.request.query_params.get("general_search")
        if general_search:
            queryset = queryset.annotate(
                fio=Concat(
                    "employee__first_name",
                    V(" "),
                    "employee__last_name",
                    V(" "),
                    "employee__patronymic",
                    output_filed=CharField(),
                )
            ).filter(Q(fio__icontains=general_search) | Q(note__icontains=general_search))

        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EmployeeNoteDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Запись по работнику"""

    serializer_class = EmployeeNoteSerializer
    queryset = EmployeeNote.objects.all()

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


class ReportCarsListView(GenericAPIView):
    """Отчет по ТС"""

    serializer_class = ReportCarSerializer

    def get_queryset(self):
        queryset = Car.objects.none()

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")
        reason_type = self.request.query_params.get("reason_type")

        if date_begin is not None and date_end is not None:
            queryset = get_report_cars_queryset(date_begin, date_end, reason_type)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReportCarsExcelView(ReportCarsListView):
    """Экспорт в Excel отчет по ТС"""

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")
        reason_type = self.request.query_params.get("reason_type")

        data = serializer.data
        if data:
            return Response(
                {"file": request.build_absolute_uri(report_cars_excel(data, date_begin, date_end, reason_type))},
                status=status.HTTP_200_OK,
            )

        return Response({"errors": {"file": ("Ошибка формирования файла!")}}, status=status.HTTP_400_BAD_REQUEST)


class ReportMechanicsListView(GenericAPIView):
    """Отчет по слесарям"""

    serializer_class = ReportMechanicsSerializer

    def get_queryset(self):
        queryset = Employee.objects.none()

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")

        if date_begin is not None and date_end is not None:
            queryset = get_report_mechanics_queryset(date_begin, date_end)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReportMechanicsExcelView(ReportMechanicsListView):
    """Экспорт в Excel отчет по слесарям"""

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")

        data = serializer.data
        if data:
            return Response(
                {"file": request.build_absolute_uri(report_mechanics_excel(data, date_begin, date_end))},
                status=status.HTTP_200_OK,
            )

        return Response({"errors": {"file": ("Ошибка формирования файла!")}}, status=status.HTTP_400_BAD_REQUEST)


class ReportMaterialsListView(GenericAPIView):
    """Отчет по материалам"""

    serializer_class = ReportMaterialSerializer

    def get_queryset(self):
        queryset = Employee.objects.none()

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")

        if date_begin is not None and date_end is not None:
            queryset = get_report_materials_queryset(date_begin, date_end)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReportMaterialsExcelView(ReportMaterialsListView):
    """Экспорт в Excel отчет по материалам"""

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")

        data = serializer.data
        if data:
            return Response(
                {"file": request.build_absolute_uri(report_materials_excel(data, date_begin, date_end))},
                status=status.HTTP_200_OK,
            )

        return Response({"errors": {"file": ("Ошибка формирования файла!")}}, status=status.HTTP_400_BAD_REQUEST)
