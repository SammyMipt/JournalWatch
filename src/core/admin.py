from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('User info', {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'is_staff',
                                  'is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'is_staff',
                       'is_superuser'),
        }),
    )


admin.site.register(User, UserAdmin)
