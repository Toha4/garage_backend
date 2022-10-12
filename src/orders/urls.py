from django.urls import path

from .api.views import OrderDetailView
from .api.views import OrderExportExcelView
from .api.views import OrderListView
from .api.views import PostDetailView
from .api.views import PostListView
from .api.views import ReasonDetailView
from .api.views import ReasonListView
from .api.views import WorkCategoryDetailView
from .api.views import WorkCategoryListView
from .api.views import WorkDetailView
from .api.views import WorkListView

urlpatterns = [
    path("api/orders/reason/", ReasonListView.as_view(), name="reason-list"),
    path("api/orders/reason/<int:pk>", ReasonDetailView.as_view(), name="reason-detail"),
    path("api/orders/post/", PostListView.as_view(), name="post-list"),
    path("api/orders/post/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("api/orders/order/", OrderListView.as_view(), name="order-list"),
    path("api/orders/order/<int:pk>", OrderDetailView.as_view(), name="order-detail"),
    path("api/orders/order/excel/", OrderExportExcelView.as_view(), name="order-excel"),
    path("api/orders/work_category/", WorkCategoryListView.as_view(), name="work-category-list"),
    path("api/orders/work_category/<int:pk>", WorkCategoryDetailView.as_view(), name="work-category-detail"),
    path("api/orders/work/", WorkListView.as_view(), name="work-list"),
    path("api/orders/work/<int:pk>", WorkDetailView.as_view(), name="work-detail"),
]
