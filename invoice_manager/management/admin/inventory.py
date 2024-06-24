from django.contrib import admin

from management.models import Category, Product, ProductSize, ProductColor, ProductTransaction
from shared.admin import BaseAdmin


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ("name",)
    filter_horizontal = ("category",)
    search_fields = ("name",)
    readonly_fields = ("total_sp_stock",)


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ("name",)


@admin.register(ProductColor)
class ProductColorAdmin(BaseAdmin):
    list_display = ("name",)


@admin.register(ProductSize)
class ProductSizeAdmin(BaseAdmin):
    list_display = ("name",)


@admin.register(ProductTransaction)
class ProductTransactionAdmin(BaseAdmin):
    list_display = ("invoice", "product", "size", "quantity", "price")
    list_filter = ("size", "created_at")
    search_fields = ("invoice_id",)
