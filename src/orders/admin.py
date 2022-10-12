from django.contrib import admin

from .models import Order
from .models import OrderWork
from .models import OrderWorkMechanic
from .models import Post
from .models import Reason
from .models import Work
from .models import WorkCategory


class ReasonAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ("number",)


class WorkCategoryAdmin(admin.ModelAdmin):
    pass


class WorkAdmin(admin.ModelAdmin):
    pass


class OrderWorkAdmin(admin.ModelAdmin):
    pass


class OrderWorkMechanicAdmin(admin.ModelAdmin):
    pass


admin.site.register(Reason, ReasonAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(WorkCategory, WorkCategoryAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(OrderWork, OrderWorkAdmin)
admin.site.register(OrderWorkMechanic, OrderWorkMechanicAdmin)
