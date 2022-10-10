from django.contrib import admin
from app_news.models import (
    CommentsModel, NewsModel
)


class NewsInline(admin.TabularInline):
    model = CommentsModel


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'get_comment']
    list_filter = ['user_name']
    actions = ['delete_admin']

    def delete_admin(self, request, queryset):
        queryset.update(comment='Удалено администратором')

    delete_admin.short_description = 'Удалить комментарий'


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date_create', 'date_edit', 'status']
    list_filter = ['status']
    inlines = [NewsInline]
    actions = ['status_as_active', 'status_as_not_active']

    def status_as_active(self, request, queryset):
        queryset.update(status=True)

    def status_as_not_active(self, request, queryset):
        queryset.update(status=False)

    status_as_active.short_description = 'Перевести в статус активна'
    status_as_not_active.short_description = 'Перевести в статус неактивна'


admin.site.register(CommentsModel, CommentsAdmin)
admin.site.register(NewsModel, NewsAdmin)