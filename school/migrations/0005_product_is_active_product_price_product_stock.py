# Generated by Django 4.2.5 on 2023-11-05 15:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0004_product_school"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="product",
            name="price",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="stock",
            field=models.IntegerField(default=0),
        ),
    ]
