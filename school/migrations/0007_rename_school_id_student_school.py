# Generated by Django 4.2.5 on 2023-11-05 15:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0006_remove_product_category_remove_product_school_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="student",
            old_name="school_id",
            new_name="school",
        ),
    ]
