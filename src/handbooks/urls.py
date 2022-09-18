from django.urls import path

from .api.views import CarDetailView
from .api.views import CarListView
from .api.views import EmployeeDetailView
from .api.views import EmployeeListView
from .api.views import PostDetailView
from .api.views import PostListView
from .api.views import ReasonDetailView
from .api.views import ReasonListView

urlpatterns = [
    path("api/handbooks/reason/", ReasonListView.as_view(), name="reason-list"),
    path("api/handbooks/reason/<int:pk>", ReasonDetailView.as_view(), name="reason-detail"),
    path("api/handbooks/post/", PostListView.as_view(), name="post-list"),
    path("api/handbooks/post/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("api/handbooks/car/", CarListView.as_view(), name="car-list"),
    path("api/handbooks/car/<int:pk>", CarDetailView.as_view(), name="car-detail"),
    path("api/handbooks/employee/", EmployeeListView.as_view(), name="employee-list"),
    path("api/handbooks/employee/<int:pk>", EmployeeDetailView.as_view(), name="employee-detail"),
]
