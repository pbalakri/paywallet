# Generated by Django 5.0.6 on 2024-07-02 02:42

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cafe", "0001_initial"),
        ("guardian", "0001_initial"),
        ("school", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Wallet",
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
                ("balance", models.FloatField(default=0)),
                ("active", models.BooleanField(default=True)),
                (
                    "bracelet",
                    models.OneToOneField(
                        default=None,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="wallet",
                        to="school.bracelet",
                    ),
                ),
            ],
            options={
                "verbose_name": "Wallet",
                "verbose_name_plural": "Wallets",
            },
        ),
        migrations.CreateModel(
            name="Transaction",
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
                (
                    "type",
                    models.CharField(
                        choices=[("credit", "credit"), ("debit", "debit")],
                        max_length=10,
                    ),
                ),
                ("amount", models.FloatField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("reference", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "merchant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="cafe.cafe"
                    ),
                ),
                (
                    "order",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="cafe.order",
                    ),
                ),
                (
                    "wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="wallet.wallet"
                    ),
                ),
            ],
            options={
                "verbose_name": "Transaction",
                "verbose_name_plural": "Transactions",
            },
        ),
        migrations.CreateModel(
            name="TopUp",
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
                ("amount", models.FloatField(default=0)),
                ("reference", models.CharField(blank=True, max_length=100, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "guardian",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="guardian.guardian",
                    ),
                ),
                (
                    "wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="wallet.wallet"
                    ),
                ),
            ],
        ),
    ]
