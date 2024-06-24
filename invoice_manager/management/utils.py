import platform

from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import admin

from weasyprint import HTML, CSS


if platform.system() == "Windows":
    import os
    os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")


@admin.action(description='Generate PDF')
def generate_invoice_pdf(modeladmin, request, queryset):
    for obj in queryset:
        # Render HTML with context data
        product_context = []
        id_counter = 0
        for invoice in obj.invoices.all():
            id_counter += 1
            product_name = invoice.product_variant.product.name
            quantity = invoice.quantity
            price = invoice.price
            rate = invoice.product_variant.price

            details = invoice.product_variant.size.name
            if invoice.product_variant.color:
                details = f"{invoice.product_variant.size.name}, {invoice.product_variant.color.name}"
            product_context.append({"product_id": id_counter, "name": product_name, "quantity": quantity, "rate": rate, "price": price, "details": details})

        html_string = render_to_string('invoice.html', {
            "customer_name": obj.user.first_name,
            "date": obj.date,
            "items": product_context,
            "subtotal": obj.subtotal,
            "delivery_charge": obj.delivery_charge,
            "advance": obj.advance,
            "net": obj.net,
            "address": obj.user.address,
            "phone": obj.user.phone_number,
            "cash_on_delivery": obj.cash_on_delivery,
        })
        # Create a PDF
        html = HTML(string=html_string)
        css = CSS(string='''
            @page {
                size: 10in 8.5in;
                margin: 0.2in;
        }
        ''')
        pdf = html.write_pdf(stylesheets=[css])

        # Create HTTP response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{obj.user.phone_number}_{obj.date}.pdf"'

        return response
