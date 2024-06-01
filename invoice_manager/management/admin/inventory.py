from django.contrib import admin

from django.contrib import messages
from django import forms
from management.models import Category, Product, ProductVariant, ProductSize, ProductColor
from shared.admin import BaseAdmin, BaseTabularInline


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ("name",)
    filter_horizontal = ("category",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ("name",)


@admin.register(ProductVariant)
class ProductVariantAdmin(BaseAdmin):
    list_display = ("product", "quantity", "price", "size", "color", "total_stock_cost")
    readonly_fields = ("total_stock_cost",)
    raw_id_fields = ("product",)
    search_fields = ("product__name",)

@admin.register(ProductColor)
class ProductColorAdmin(BaseAdmin):
    list_display = ("name",)

@admin.register(ProductSize)
class ProductSizeAdmin(BaseAdmin):
    list_display = ("name",)
