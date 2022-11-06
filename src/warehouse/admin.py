from django.contrib import admin

from .models import Entrance
from .models import Material
from .models import MaterialCategory
from .models import Turnover
from .models import Unit
from .models import Warehouse


class WarehouseAdmin(admin.ModelAdmin):
    pass


class UnitAdmin(admin.ModelAdmin):
    pass


class MaterialCategoryAdmin(admin.ModelAdmin):
    pass


class MaterialAdmin(admin.ModelAdmin):
    pass


class EntranceAdmin(admin.ModelAdmin):
    pass


class TurnoverMaterialAdmin(admin.ModelAdmin):
    pass


admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(MaterialCategory, MaterialCategoryAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Entrance, EntranceAdmin)
admin.site.register(Turnover, TurnoverMaterialAdmin)
