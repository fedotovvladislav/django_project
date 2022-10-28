from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    CommentsModel, NewsModel, User)


@admin.register(CommentsModel)
class CommentsAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class MyUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name",
                                         "email", "phone", "city")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
