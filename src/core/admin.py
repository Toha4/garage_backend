from django.contrib import admin

from .models import Car
from .models import Employee


class CarAdmin(admin.ModelAdmin):
    readonly_fields = (
        "kod_mar_in_putewka",
        "gos_nom_in_putewka",
        "state_number",
        "kod_driver",
        "date_decommissioned",
    )


class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = (
        "number_in_kadry",
        "first_name",
        "last_name",
        "patronymic",
        "position",
        "date_dismissal",
    )


admin.site.register(Car, CarAdmin)
admin.site.register(Employee, EmployeeAdmin)
