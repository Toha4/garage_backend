from django.urls import path

from .api.views import CarTaskDetailView
from .api.views import CarTaskExcelView
from .api.views import CarTaskListView

urlpatterns = [
    path("api/car_tasks/car_tasks/", CarTaskListView.as_view(), name="car-tasks-list"),
    path("api/car_tasks/car_tasks/<int:pk>", CarTaskDetailView.as_view(), name="car-tasks-detail"),
    path("api/car_tasks/car_tasks/excel/", CarTaskExcelView.as_view(), name="car-tasks-excel"),
]
