from django.contrib import admin

from .models import CarTask


class CarTaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(CarTask, CarTaskAdmin)
