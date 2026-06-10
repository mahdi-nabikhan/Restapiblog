from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'is_superuser', 'is_active',)
    list_filter = ('is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions','is_verified')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser','is_verified '),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
