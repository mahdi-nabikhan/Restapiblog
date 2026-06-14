from django.contrib import admin
from .models import Post, Category, Comments


# =========================
# CATEGORY ADMIN
# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# =========================
# POST ADMIN
# =========================
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "auther",
        "category",
        "status",
        "published_date",
        "created_date",
    )

    list_filter = (
        "status",
        "category",
        "created_date",
        "published_date",
    )

    search_fields = (
        "title",
        "content",
        "auther__email",
        "category__name",
    )

    readonly_fields = (
        "created_date",
        "updated_date",
    )

    fieldsets = (
        ("Main Info", {
            "fields": ("title", "content", "image")
        }),
        ("Relations", {
            "fields": ("auther", "category")
        }),
        ("Status", {
            "fields": ("status", "published_date")
        }),
        ("Timestamps", {
            "fields": ("created_date", "updated_date")
        }),
    )

    ordering = ("-created_date",)


# =========================
# COMMENTS ADMIN
# =========================
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "post",
        "published",
        "created_at",
    )

    list_filter = (
        "published",
        "created_at",
    )

    search_fields = (
        "user__email",
        "post__title",
        "content",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Relation", {
            "fields": ("user", "post")
        }),
        ("Content", {
            "fields": ("content",)
        }),
        ("Status", {
            "fields": ("published",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )

    ordering = ("-created_at",)