from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "email",
        "is_superuser",
        "is_active",
    )
    list_filter = ("is_superuser", "is_active")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "is_verified",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified ",
                ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "first_name",
        "last_name",
        "updated_date",
    )

    list_filter = (
        "created_date",
        "updated_date",
    )

    search_fields = (
        "user__email",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "created_date",
        "updated_date",
    )

    fieldsets = (
        ("User Info", {"fields": ("user",)}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "image", "description")},
        ),
        ("Timestamps", {"fields": ("created_date", "updated_date")}),
    )

    ordering = ("-updated_date",)


admin.site.register(User, CustomUserAdmin)
