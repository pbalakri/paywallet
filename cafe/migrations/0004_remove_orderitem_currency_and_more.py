# Generated by Django 4.2.5 on 2024-03-06 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0003_remove_orderitem_product_name_orderitem_product"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="currency",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="original_price",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="selling_price",
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="product",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.RESTRICT,
                to="cafe.inventory",
            ),
        ),
    ]
