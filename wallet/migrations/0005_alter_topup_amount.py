# Generated by Django 4.2.5 on 2024-04-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallet", "0004_topup"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topup",
            name="amount",
            field=models.FloatField(default=0),
        ),
    ]
