# Generated by Django 5.0.6 on 2024-07-02 02:13

import django.db.models.deletion
import paywallet.storage_backends
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("school", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Guardian",
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
                ("phone_number", models.CharField(max_length=100)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        storage=paywallet.storage_backends.PublicMediaStorage,
                        upload_to="guardian/",
                    ),
                ),
                ("student", models.ManyToManyField(blank=True, to="school.student")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Device",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("device_fcm_token", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "guardian",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="guardian_user",
                        to="guardian.guardian",
                    ),
                ),
            ],
            options={
                "verbose_name": "Device",
                "verbose_name_plural": "Devices",
            },
        ),
    ]
