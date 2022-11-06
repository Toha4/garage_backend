from django.urls import path

from .api.views import CarDetailView
from .api.views import CarListView
from .api.views import CarTagsListView
from .api.views import EmployeeDetailView
from .api.views import EmployeeListView

urlpatterns = [
    path("api/core/car/", CarListView.as_view(), name="car-list"),
    path("api/core/car/<int:pk>", CarDetailView.as_view(), name="car-detail"),
    path("api/core/car/tags/", CarTagsListView.as_view(), name="car-tag-list"),
    path("api/core/employee/", EmployeeListView.as_view(), name="employee-list"),
    path("api/core/employee/<int:pk>", EmployeeDetailView.as_view(), name="employee-detail"),
]
