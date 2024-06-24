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
    quantity = models.PositiveIntegerField(default=0, verbose_name="quantity")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="price")
    total_sp_stock = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True, verbose_name="total selling price")
    description = models.TextField(null=True, blank=True, verbose_name="description")

    def __str__(self) -> str:
        return f"{self.name}"


    def save(self, *args, **kwargs) -> None:
        self.total_sp_stock = self.selling_price * self.quantity
        return super().save(*args, **kwargs)


class ProductSize(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="name")

    def __str__(self) -> str:
        return self.name    


class ProductColor(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="name")

    def __str__(self) -> str:
        return self.name


class ProductTransaction(BaseModel):
    invoice = models.ForeignKey("Invoice", on_delete=models.PROTECT, related_name="invoice_transactions")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product_transactions")
    size = models.ForeignKey(ProductSize, on_delete=models.PROTECT, related_name="size_transactions")
    quantity = models.PositiveIntegerField(default=0, verbose_name="quantity")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="price")

    def __str__(self) -> str:
        return f"{self.product.name}"
