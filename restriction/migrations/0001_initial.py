# Generated by Django 5.0.6 on 2024-07-02 04:12

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product", "0001_initial"),
        ("school", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryRestriction",
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
                ("total_per_period", models.FloatField(default=3)),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("Weekly", "Weekly"),
                            ("Daily", "Daily"),
                            ("Monthly", "Monthly"),
                        ],
                        default="Weekly",
                        max_length=10,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.category",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="school.student",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category Restriction",
                "verbose_name_plural": "Category Restrictions",
            },
        ),
        migrations.CreateModel(
            name="DietRestriction",
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
                ("allergies", models.ManyToManyField(blank=True, to="product.allergy")),
                (
                    "student",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="school.student",
                    ),
                ),
            ],
            options={
                "verbose_name": "Diet Restriction",
                "verbose_name_plural": "Diet Restrictions",
            },
        ),
        migrations.CreateModel(
            name="PaymentRestriction",
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
                ("total_per_period", models.FloatField(default=3)),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("Weekly", "Weekly"),
                            ("Daily", "Daily"),
                            ("Monthly", "Monthly"),
                        ],
                        default="Weekly",
                        max_length=10,
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="school.student",
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment Restriction",
                "verbose_name_plural": "Payment Restrictions",
            },
        ),
        migrations.CreateModel(
            name="ProductsRestriction",
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
                ("total_per_period", models.FloatField(default=3)),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("Weekly", "Weekly"),
                            ("Daily", "Daily"),
                            ("Monthly", "Monthly"),
                        ],
                        default="Weekly",
                        max_length=10,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="school.student",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Restriction",
                "verbose_name_plural": "Product Restrictions",
            },
        ),
    ]
