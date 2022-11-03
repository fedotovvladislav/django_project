from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.User)
class MyUserAdmin(UserAdmin):
    model = models.User
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name",
                                         "email", "phone", "avatar")}),
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
    list_display = ("avatar_tag", "username", "email", "first_name", "last_name", "is_staff")


@admin.register(models.BlogModel)
class BlogAdmin(admin.ModelAdmin):
    model = models.BlogModel
    list_display = ('id', 'user', 'summary_description')