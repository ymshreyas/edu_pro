# Generated by Django 4.1 on 2023-08-12 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edu_app", "0006_remove_detailed_cie_finalise"),
    ]

    operations = [
        migrations.AddField(
            model_name="detailed_cie",
            name="total",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
