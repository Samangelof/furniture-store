from django.contrib import admin
from .models import (
    Mebels,
    Order,
    OrderItem,
    SubCategory,
    MebelImage
)


admin.site.register(Mebels)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(SubCategory)
admin.site.register(MebelImage)

