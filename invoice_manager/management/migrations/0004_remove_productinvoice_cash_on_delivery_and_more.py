# Generated by Django 5.0.6 on 2024-05-30 17:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0003_productinvoice_cash_on_delivery"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productinvoice",
            name="cash_on_delivery",
        ),
        migrations.AddField(
            model_name="invoice",
            name="cash_on_delivery",
            field=models.BooleanField(default=False, verbose_name="cash on delivery"),
        ),
    ]
