# Generated by Django 5.0.6 on 2024-07-02 02:13

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product", "0001_initial"),
        ("school", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Cafe",
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
                ("name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=100)),
                (
                    "admin",
                    models.OneToOneField(
                        limit_choices_to={"groups__name": "Vendor Admin"},
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="vendor_admin",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "operators",
                    models.ManyToManyField(
                        limit_choices_to={
                            "groups__name__in": ["Vendor Admin", "Vendor Operator"]
                        },
                        related_name="vendor_users",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "school",
                    models.OneToOneField(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="school.school",
                    ),
                ),
            ],
            options={
                "verbose_name": "Café",
                "verbose_name_plural": "Café",
                "unique_together": {("name", "address")},
            },
        ),
        migrations.CreateModel(
            name="Inventory",
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
                (
                    "product_code",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("quantity", models.IntegerField()),
                ("date", models.DateField(auto_now_add=True)),
                ("price", models.FloatField()),
                (
                    "cafe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="cafe.cafe"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="product.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Inventory",
                "verbose_name_plural": "Inventory",
                "unique_together": {("product_code", "cafe")},
            },
        ),
        migrations.CreateModel(
            name="Operator",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("phone", models.CharField(max_length=20)),
                (
                    "cafe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cafe.cafe"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Operator",
                "verbose_name_plural": "Operators",
            },
        ),
        migrations.CreateModel(
            name="Order",
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
                    "cafe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="cafe.cafe"
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("quantity", models.IntegerField()),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cafe.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="cafe.inventory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order Item",
                "verbose_name_plural": "Order Items",
            },
        ),
        migrations.CreateModel(
            name="VendorAdmin",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("phone", models.CharField(max_length=20)),
                (
                    "user",
                    models.OneToOneField(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Vendor Administrator",
                "verbose_name_plural": "Vendor Administrators",
            },
        ),
    ]
