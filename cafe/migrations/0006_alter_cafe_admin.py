# Generated by Django 4.2.5 on 2024-03-11 08:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cafe", "0005_vendoradmin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cafe",
            name="admin",
            field=models.OneToOneField(
                limit_choices_to={"groups__name": "Vendor Admin"},
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="vendor_admin",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
