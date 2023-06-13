from django.contrib import admin
from .models import Product
from admin_mixins import ExportAsCSVMixin


@admin.register(Product)
class ProductModel(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        "export_csv"
    ]
    list_display = ["pk", "name", "description_short", "price"]
    list_display_links = ["pk", "name"]
