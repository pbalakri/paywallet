# Generated by Django 5.0.6 on 2024-07-02 02:13

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("guardian", "0001_initial"),
        ("school", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("name_en", models.CharField(max_length=100, null=True)),
                ("name_ar", models.CharField(max_length=100, null=True)),
                (
                    "parent_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="school_store.category",
                    ),
                ),
                (
                    "school",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="school.school",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
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
                ("date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Ready for Pickup", "Ready for Pickup"),
                            ("Completed", "Completed"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="guardian.guardian",
                    ),
                ),
                (
                    "school",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="school.school",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "name_en",
                    models.CharField(max_length=100, null=True, verbose_name="Name"),
                ),
                (
                    "name_ar",
                    models.CharField(max_length=100, null=True, verbose_name="Name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "description_en",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "description_ar",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, upload_to="products/", verbose_name="Image"
                    ),
                ),
                ("price", models.FloatField(default=0, verbose_name="Price")),
                ("stock", models.IntegerField(default=0, verbose_name="Stock")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="school_store.category",
                        verbose_name="Category",
                    ),
                ),
                (
                    "school",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="school.school",
                        verbose_name="School",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
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
                ("quantity", models.IntegerField(default=0)),
                ("unit_price", models.FloatField(default=0)),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="orderitem_set",
                        to="school_store.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="school_store.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order Item",
                "verbose_name_plural": "Order Items",
            },
        ),
    ]
