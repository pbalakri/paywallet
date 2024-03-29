# Generated by Django 4.2.5 on 2024-03-16 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0004_alter_product_options"),
        ("restriction", "0004_categoryrestriction_count_per_period_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productrestriction",
            name="product",
        ),
        migrations.AddField(
            model_name="productrestriction",
            name="product",
            field=models.ForeignKey(
                blank=True,
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="product.product",
            ),
            preserve_default=False,
        ),
    ]
