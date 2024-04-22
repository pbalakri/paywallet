# Generated by Django 4.2.5 on 2024-04-22 05:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restriction", "0009_remove_categoryrestriction_count_per_period_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categoryrestriction",
            name="total_per_period",
            field=models.FloatField(default=3),
        ),
        migrations.AlterField(
            model_name="paymentrestriction",
            name="total_per_period",
            field=models.FloatField(default=3),
        ),
        migrations.AlterField(
            model_name="productsrestriction",
            name="total_per_period",
            field=models.FloatField(default=3),
        ),
    ]
