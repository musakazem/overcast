from typing import Iterable
from django.db import models

from shared.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=50, verbose_name="name")
    description = models.TextField(null=True, blank=True, verbose_name="description")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    category = models.ManyToManyField(Category, verbose_name="category")
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, verbose_name="description")

    def __str__(self) -> str:
        return f"{self.name}"


class ProductSize(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="name")

    def __str__(self) -> str:
        return self.name    


class ProductColor(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="name")

    def __str__(self) -> str:
        return self.name


class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="quantity")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="price")
    total_stock_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True, verbose_name="total price")

    size = models.ForeignKey(ProductSize, on_delete=models.PROTECT, related_name="size_product_variants", verbose_name="size")
    color = models.ForeignKey(ProductColor, on_delete=models.PROTECT, null=True, blank=True, related_name="color_product_variants", verbose_name="color")

    def __str__(self) -> str:
        title = f"{self.product.name} {self.size.name}"
        return f"{title}, {self.color.name}" if self.color else title

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        self.total_stock_cost = self.price * self.quantity
        return super().save(*args, **kwargs)