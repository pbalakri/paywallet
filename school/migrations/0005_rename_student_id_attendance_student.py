# Generated by Django 4.2.5 on 2024-03-08 05:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0004_alter_teacher_bracelet"),
    ]

    operations = [
        migrations.RenameField(
            model_name="attendance",
            old_name="student_id",
            new_name="student",
        ),
    ]
