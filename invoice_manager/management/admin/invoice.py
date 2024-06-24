from django.db import transaction
from django.contrib import admin, messages
from django import forms

from dal import autocomplete
from management.models import InvoiceCounter, Product, ProductTransaction

from shared.admin import BaseAdmin, BaseTabularInline
from management.models import ProductInvoice, Invoice, InvoiceCounter
# from management.utils import generate_invoice_pdf


class ProductInvoiceInline(BaseTabularInline):
    model = ProductInvoice
    readonly_fields = ("price",)
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ("product_unit_price",)
        return readonly_fields

    def product_unit_price(self, obj):
        return obj.price

    product_unit_price.short_description = 'unit price' 

class PersonForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('__all__')
        widgets = {
            'user': autocomplete.ModelSelect2(url='user-autocomplete')
        }

@admin.register(Invoice)
class InvoiceAdmin(BaseAdmin):
    inlines = (ProductInvoiceInline,)
    form = PersonForm
    list_display = ("user", "subtotal", "delivery_charge", "net", "created_at", "transaction_successful")
    readonly_fields = ("subtotal", "net", "counter", "transaction_successful")
    exclude = ("archived", "creator")

    search_fields = ("user__phone_number",)
    list_filter = ("created_at",)

    def save_formset(self, request, form, formset, change):
        formset.save()
        prices = form.instance.invoices.values_list("price", flat=True)
        subtotal = sum(prices)
        form.instance.subtotal = subtotal

        net = (subtotal + form.instance.delivery_charge) - form.instance.advance

        form.instance.net = net
        form.instance.save()

    def run_transaction(self, request, queryset):
        try:
            with transaction.atomic():
                for invoice in queryset:
                    product_invoices = ProductInvoice.objects.filter(invoice_id=invoice.id)
                    products = []
                    product_transactions = []
                    for product_invoice in product_invoices:
                        updated_product_quantity = product_invoice.product.quantity - product_invoice.quantity

                        product = Product(id=product_invoice.product.id, quantity=updated_product_quantity)

                        products.append(product)
                        product_transaction = ProductTransaction(
                            invoice=invoice,
                            product=product_invoice.product,
                            size=product_invoice.size,
                            quantity=product_invoice.quantity,
                            price=product_invoice.price,
                        )
                        product_transactions.append(product_transaction)
                    ProductTransaction.objects.bulk_create(product_transactions)
                    Product.objects.bulk_update(products, ["quantity"])
                    queryset.update(transaction_successful=True)

            self.message_user(request, "Transaction Successful", level=messages.INFO)
        except Exception as e:
            self.message_user(request, f"An unexpected error occurred: {str(e)}", level=messages.ERROR)

    actions = [run_transaction]

@admin.register(InvoiceCounter)
class InvoiceCounterAdmin(BaseAdmin):
    list_display = ("counter",)

    def has_add_permission(self, request):
        return not InvoiceCounter.objects.all().count() == 1

    def has_delete_permission(self, request, obj=None):
        return False
