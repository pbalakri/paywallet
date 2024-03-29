# Generated by Django 4.2.5 on 2024-03-16 06:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0015_alter_student_image"),
        ("product", "0004_alter_product_options"),
        ("restriction", "0007_remove_productrestriction_product_and_more"),
    ]

    operations = [
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
                ("count_per_period", models.IntegerField(default=3)),
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
        migrations.DeleteModel(
            name="ProductRestriction",
        ),
    ]
