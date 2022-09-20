from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from app.helpers.database import get_period_filter_lookup
from app.views import EagerLoadingMixin
from orders.helpers.order_general_search import order_general_search

from ..models import Order
from ..models import Post
from ..models import Reason
from ..models import Work
from ..models import WorkCategory
from .serializers import OrderDetailSerializer
from .serializers import OrderListSerializer
from .serializers import PostSerializer
from .serializers import ReasonSerializer
from .serializers import WorkCategorySerializer
from .serializers import WorkSerializer


class ReasonListView(CreateModelMixin, GenericAPIView):
    """Список причин"""

    serializer_class = ReasonSerializer
    queryset = Reason.objects.all()

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

    serializer_class = PostSerializer
    queryset = Post.objects.all()

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

        reasons = self.request.query_params.get("reasons")
        if reasons:
            queryset = queryset.filter(reason__pk__in=[int(reason) for reason in reasons.split(",")])

        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)

        date_begin = self.request.query_params.get("date_begin")
        date_end = self.request.query_params.get("date_end")
        if date_begin or date_end:
            queryset = queryset.filter(get_period_filter_lookup("date_begin", date_begin, date_end, True))

        general_search = self.request.query_params.get("general_search")
        if general_search:
            queryset = order_general_search(queryset, str(general_search))

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


class WorkCategoryListView(CreateModelMixin, GenericAPIView):
    """Список категорий работ"""

    serializer_class = WorkCategorySerializer
    queryset = WorkCategory.objects.all()

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
    """

    serializer_class = WorkSerializer
    queryset = Work.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__pk=category)

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
