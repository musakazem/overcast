from typing import Iterable
from django.db import models

from shared.models import BaseModel, SingletonModel
from user.models import User


class InvoiceCounter(SingletonModel):
    counter = models.PositiveIntegerField(default=0, verbose_name="counter")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.counter)


class Invoice(BaseModel):
    user = models.ForeignKey(User, related_name="invoices", on_delete=models.PROTECT, verbose_name="user")
    counter = models.ForeignKey(InvoiceCounter, on_delete=models.PROTECT, verbose_name="counter", default=1)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="delivery charge")
    advance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="advance")
    subtotal = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name="subtotal")
    net = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name="net")
    cash_on_delivery = models.BooleanField(default=False, verbose_name="cash on delivery")
    transaction_successful = models.BooleanField(default=False, verbose_name="transaction successful")

    def __str__(self) -> str:
        return self.user.phone_number

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.counter.counter += 1
            self.counter.save()
            return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)


class ProductInvoice(BaseModel):
    product = models.ForeignKey("Product", on_delete=models.PROTECT, related_name="product_invoices", verbose_name="product", default=0)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoices", verbose_name="invoice")
    size = models.ForeignKey("ProductSize", on_delete=models.PROTECT, related_name="size_product_invoices", verbose_name="size", default=0)
    quantity = models.PositiveIntegerField(default=0, verbose_name="quantity")
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name="price")

    def save(self, *args, **kwargs):
        if self.product.quantity <= 0:
            return

        self.price = self.product.selling_price * self.quantity
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.name} {self.size.name}"
