from django.contrib import admin
from django import forms

from dal import autocomplete

from shared.admin import BaseAdmin, BaseTabularInline
from management.models import ProductInvoice, Invoice
from management.utils import generate_invoice_pdf


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
        return obj.product_variant.price

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
    list_display = ("user", "subtotal", "delivery_charge", "net", "date")
    readonly_fields = ("subtotal", "net")
    exclude = ("archived", "creator")

    search_fields = ("user__phone_number",)
    list_filter = ("date",)
    actions = [generate_invoice_pdf]

    def save_formset(self, request, form, formset, change):
        formset.save()
        prices = form.instance.invoices.values_list("price", flat=True)
        subtotal = sum(prices)
        form.instance.subtotal = subtotal

        net = (subtotal + form.instance.delivery_charge) - form.instance.advance

        form.instance.net = net
        form.instance.save()
