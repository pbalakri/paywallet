# Generated by Django 4.2.5 on 2024-03-10 03:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restriction", "0003_remove_productrestriction_product_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="categoryrestriction",
            name="count_per_period",
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name="categoryrestriction",
            name="frequency",
            field=models.CharField(
                choices=[
                    ("Weekly", "Weekly"),
                    ("Daily", "Daily"),
                    ("Monthly", "Monthly"),
                ],
                default="Weekly",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="productrestriction",
            name="count_per_period",
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name="productrestriction",
            name="frequency",
            field=models.CharField(
                choices=[
                    ("Weekly", "Weekly"),
                    ("Daily", "Daily"),
                    ("Monthly", "Monthly"),
                ],
                default="Weekly",
                max_length=10,
            ),
        ),
    ]
