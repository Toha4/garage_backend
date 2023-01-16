from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin

from app.views import EagerLoadingMixin

from ..models import CarTask
from .serializers import CarTaskListSerializer
from .serializers import CarTaskSerializer


class CarTaskListView(EagerLoadingMixin, ListAPIView, CreateModelMixin):
    """
    Список планируемых задач

    Filters: car(int), order_created(int), show_completed(bool)
    General search(str): description, materials
    """

    queryset = CarTask.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CarTaskListSerializer
        return CarTaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        car = self.request.query_params.get("car")
        if car:
            queryset = queryset.filter(car=car)

        order_created = self.request.query_params.get("order_created")
        show_completed = self.request.query_params.get("show_completed")
        if not show_completed or show_completed != "true":
            # Если запрошенный список для заказ-наряда, то задачи созданные в нем отображаем в любом случае
            if order_created:
                queryset = queryset.filter(Q(is_completed=False) | Q(order=order_created))
            else:
                queryset = queryset.filter(is_completed=False)

        general_search = self.request.query_params.get("general_search")
        if general_search:
            queryset = queryset.filter(
                Q(description__icontains=general_search) | Q(materials__icontains=general_search)
            )

        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CarTaskDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Планираемая задача"""

    serializer_class = CarTaskSerializer
    queryset = CarTask.objects.all()

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

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
