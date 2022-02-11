from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from core.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    order = ('-start_date',)
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('email', 'first_name', 'last_name')
    fieldsets = (
        (
            None, {
                'fields': ('email', 'first_name', 'last_name',)
                }
        ),
        (
            'Permissions', {
                'fields': ('is_staff', 'is_active')
            }
        )
    )
