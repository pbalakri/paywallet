# Generated by Django 4.2.5 on 2023-11-05 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0006_remove_product_category_remove_product_school_and_more"),
        ("school_store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="school",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="school.school",
            ),
        ),
    ]
