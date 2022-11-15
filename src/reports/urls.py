from django.urls import path

from .api.views import EmployeeNoteDetailView
from .api.views import EmployeeNoteListView
from .api.views import ReportCarsExcelView
from .api.views import ReportCarsListView
from .api.views import ReportMaterialsExcelView
from .api.views import ReportMaterialsListView
from .api.views import ReportMechanicsExcelView
from .api.views import ReportMechanicsListView

urlpatterns = [
    path("api/reports/employee_notes/", EmployeeNoteListView.as_view(), name="reports-employee-notes-list"),
    path(
        "api/reports/employee_notes/<int:pk>", EmployeeNoteDetailView.as_view(), name="reports-employee-notes-detail"
    ),
    path("api/reports/cars/", ReportCarsListView.as_view(), name="reports-cars-list"),
    path("api/reports/cars/excel/", ReportCarsExcelView.as_view(), name="reports-cars-excel"),
    path("api/reports/mechanics/", ReportMechanicsListView.as_view(), name="reports-mechanics-list"),
    path("api/reports/mechanics/excel/", ReportMechanicsExcelView.as_view(), name="reports-mechanics-excel"),
    path("api/reports/materials/", ReportMaterialsListView.as_view(), name="reports-materials-list"),
    path("api/reports/materials/excel/", ReportMaterialsExcelView.as_view(), name="reports-materials-excel"),
]
