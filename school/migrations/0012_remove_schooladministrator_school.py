# Generated by Django 4.2.5 on 2024-03-11 07:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0011_alter_bracelet_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="schooladministrator",
            name="school",
        ),
    ]
