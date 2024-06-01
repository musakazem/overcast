from django.db import models

from shared.models import BaseModel
from user.models import User


class Invoice(BaseModel):
    user = models.ForeignKey(User, related_name="invoices", on_delete=models.PROTECT, verbose_name="user")
    date = models.DateField()
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="delivery charge")
    advance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="advance")
    subtotal = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name="subtotal")
    net = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name="net")
    cash_on_delivery = models.BooleanField(default=False, verbose_name="cash on delivery")

    def __str__(self) -> str:
        return self.user.phone_number

class ProductInvoice(BaseModel):
    product_variant = models.ForeignKey("ProductVariant", on_delete=models.PROTECT, related_name="product_invoices", verbose_name="product")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoices", verbose_name="invoice")
    quantity = models.PositiveIntegerField(verbose_name="quantity")
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name="price")

    def save(self, *args, **kwargs):
        self.price = self.product_variant.price * self.quantity
        return super().save(*args, **kwargs)
