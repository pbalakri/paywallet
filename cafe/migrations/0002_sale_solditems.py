# Generated by Django 4.2.5 on 2023-11-04 11:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sale",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                ("total", models.FloatField()),
                ("currency", models.CharField(default="KWD", max_length=10)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("cash", "Cash"),
                            ("card", "Card"),
                            ("points", "Points"),
                        ],
                        default="cash",
                        max_length=10,
                    ),
                ),
                (
                    "cafe_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="cafe.cafe"
                    ),
                ),
            ],
            options={
                "verbose_name": "Sale",
                "verbose_name_plural": "Sales",
            },
        ),
        migrations.CreateModel(
            name="SoldItems",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("product_name", models.CharField(max_length=100)),
                ("quantity", models.IntegerField()),
                ("originalPrice", models.FloatField()),
                ("sellingPrice", models.FloatField()),
                ("currency", models.CharField(default="KWD", max_length=10)),
                (
                    "sale_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cafe.sale"
                    ),
                ),
            ],
            options={
                "verbose_name": "Sold Item",
                "verbose_name_plural": "Sold Items",
            },
        ),
    ]
