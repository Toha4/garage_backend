from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from app.helpers.database import get_period_filter_lookup
from app.views import EagerLoadingMixin

from ..helpers.order_general_search import order_general_search
from ..models import Order
from ..models import Post
from ..models import Reason
from ..models import Work
from ..models import WorkCategory
from ..reports.order_excel import OrderExcelCreator
from .serializers import OrderDetailSerializer
from .serializers import OrderListSerializer
from .serializers import PostListSerializer
from .serializers import PostSerializer
from .serializers import ReasonListSerializer
from .serializers import ReasonSerializer
from .serializers import WorkCategoryListSerializer
from .serializers import WorkCategorySerializer
from .serializers import WorkListSerializer
from .serializers import WorkSerializer


class ReasonListView(CreateModelMixin, GenericAPIView):
    """Список причин"""

    serializer_class = ReasonSerializer
    queryset = Reason.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReasonListSerializer
        return ReasonSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        search_name = self.request.query_params.get("search_name")
        if search_name:
            queryset = queryset.filter(name__icontains=search_name)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReasonDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Причина"""

    serializer_class = ReasonSerializer
    queryset = Reason.objects.all()

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


class PostListView(CreateModelMixin, GenericAPIView):
    """Список постов"""

    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostListSerializer
        return PostSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Пост"""

    serializer_class = PostSerializer
    queryset = Post.objects.all()

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


class OrderListView(EagerLoadingMixin, ListAPIView, CreateModelMixin):
    """
    Список заказ-нарядов

    Filters: reasons(list(int)), status(int), date_begin(date_str), date_end(date_str)
    Search's: general_search (number, car__state_number, car__name, note)
    """

    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderListSerializer
        return OrderDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        reason_type = self.request.query_params.get("reason_type")
        if reason_type:
            queryset = queryset.filter(reason__type=reason_type)

        statuses = self.request.query_params.get("statuses")
        if statuses:
            queryset = queryset.filter(status__in=[int(status) for status in statuses.split(",")])

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")
        if date_begin or date_end:
            queryset = queryset.filter(get_period_filter_lookup("date_begin", date_begin, date_end, True))

        general_search = self.request.query_params.get("general_search")
        if general_search:
            queryset = order_general_search(queryset, str(general_search))

        sort_field = self.request.query_params.get("sortField")
        sort_order = self.request.query_params.get("sortOrder")
        if sort_field and sort_order:
            sort_order = "-" if sort_order == "descend" else ""
            queryset = queryset.order_by(f"{sort_order}{sort_field}", "pk")

        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrderDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Заказ-наряд"""

    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()

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


class OrderExportExcelView(GenericAPIView):
    """Экспорт в Excel заказ-наряда"""
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):     
        try:
            order = None
            pk = self.request.query_params.get("pk")
            if pk:    
                order = self.get_queryset().get(pk=pk)

            return Response({"file": request.build_absolute_uri(OrderExcelCreator(order)())}, status=status.HTTP_200_OK)
            
        except Exception:
            return Response({"errors": {"file": ("Ошибка формирования файла!")}}, status=status.HTTP_400_BAD_REQUEST)


class WorkCategoryListView(CreateModelMixin, GenericAPIView):
    """Список категорий работ"""

    queryset = WorkCategory.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WorkCategoryListSerializer
        return WorkCategorySerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class WorkCategoryDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Категория работ"""

    serializer_class = WorkCategorySerializer
    queryset = WorkCategory.objects.all()

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


class WorkListView(CreateModelMixin, GenericAPIView):
    """
    Список работ

    Filters: category(int)
    Search's: name
    """

    queryset = Work.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return WorkListSerializer
        return WorkSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__pk=category)

        search_name = self.request.query_params.get("search_name")
        if search_name:
            queryset = queryset.filter(name__icontains=search_name)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class WorkDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Работа"""

    serializer_class = WorkSerializer
    queryset = Work.objects.all()

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
