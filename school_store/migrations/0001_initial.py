# Generated by Django 4.2.5 on 2023-11-05 15:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("school", "0006_remove_product_category_remove_product_school_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name_plural": "Categories",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("image", models.ImageField(blank=True, upload_to="products/")),
                ("price", models.FloatField(default=0)),
                ("stock", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "category",
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
        ),
    ]
