from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_staff',)
    list_filter = ('email',)


admin.site.register(CustomUser, UserAdmin)