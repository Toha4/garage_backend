from django.urls import path

from .api.views import EntranceDetailView
from .api.views import EntranceListView
from .api.views import MaterialCategoryDetailView
from .api.views import MaterialCategoryListView
from .api.views import MaterialDetailView
from .api.views import MaterialListView
from .api.views import MaterialRemainsCategoryListView
from .api.views import MaterialRemainsListView
from .api.views import ProviderListView
from .api.views import TurnoverDetailView
from .api.views import TurnoverListView
from .api.views import TurnoverMaterialListView
from .api.views import TurnoverMovingMaterialView
from .api.views import UnitDetailView
from .api.views import UnitListView
from .api.views import WarehouseDetailView
from .api.views import WarehouseListView

urlpatterns = [
    path("api/warehouse/warehouse/", WarehouseListView.as_view(), name="warehouse-list"),
    path("api/warehouse/warehouse/<int:pk>", WarehouseDetailView.as_view(), name="warehouse-detail"),
    path("api/warehouse/unit/", UnitListView.as_view(), name="unit-list"),
    path("api/warehouse/unit/<int:pk>", UnitDetailView.as_view(), name="unit-detail"),
    path("api/warehouse/material_category/", MaterialCategoryListView.as_view(), name="material-category-list"),
    path("api/warehouse/material_category/<int:pk>", MaterialCategoryDetailView.as_view(), name="material-category-detail"),
    path("api/warehouse/material/", MaterialListView.as_view(), name="material-list"),
    path("api/warehouse/material/remains/", MaterialRemainsListView.as_view(), name="material-remains-list"),
    path("api/warehouse/material/remains_category/", MaterialRemainsCategoryListView.as_view(), name="material-remains-category-list"),
    path("api/warehouse/material/<int:pk>", MaterialDetailView.as_view(), name="material-detail"),
    path("api/warehouse/entrance/", EntranceListView.as_view(), name="entrance-list"),
    path("api/warehouse/entrance/<int:pk>", EntranceDetailView.as_view(), name="entrance-detail"),
    path("api/warehouse/entrance/providers/", ProviderListView.as_view(), name="entrance-provider-list"),
    path("api/warehouse/turnover/", TurnoverListView.as_view(), name="turnover-list"),
    path("api/warehouse/turnover/<int:pk>", TurnoverDetailView.as_view(), name="turnover-detail"),
    path("api/warehouse/turnover/material/", TurnoverMaterialListView.as_view(), name="turnover-material-list"),
    path("api/warehouse/turnover/moving_material/", TurnoverMovingMaterialView.as_view(), name="turnover-moving-material"),
]
