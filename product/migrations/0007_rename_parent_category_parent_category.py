# Generated by Django 4.2.5 on 2023-11-07 07:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0006_category_parent"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category",
            old_name="parent",
            new_name="parent_category",
        ),
    ]