# Generated by Django 4.1 on 2023-08-12 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edu_app", "0005_detailed_cie_finalise"),
    ]

    operations = [
        migrations.RemoveField(model_name="detailed_cie", name="finalise",),
    ]
