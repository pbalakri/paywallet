# Generated by Django 4.2.5 on 2024-03-16 05:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0004_alter_product_options"),
        ("restriction", "0006_alter_productrestriction_product"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productrestriction",
            name="product",
        ),
        migrations.AddField(
            model_name="productrestriction",
            name="product",
            field=models.ManyToManyField(blank=True, to="product.product"),
        ),
    ]
