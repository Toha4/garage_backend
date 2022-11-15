from django.contrib import admin

from .models import EmployeeNote


class EmployeeNoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(EmployeeNote, EmployeeNoteAdmin)
