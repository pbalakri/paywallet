# Generated by Django 4.2.5 on 2024-03-11 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0012_remove_schooladministrator_school"),
    ]

    operations = [
        migrations.AlterField(
            model_name="school",
            name="school_admin",
            field=models.OneToOneField(
                limit_choices_to={"groups__name": "School Admin"},
                on_delete=django.db.models.deletion.RESTRICT,
                to=settings.AUTH_USER_MODEL,
                verbose_name="School Admin",
            ),
        ),
    ]
