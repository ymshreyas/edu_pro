# Generated by Django 4.1 on 2023-08-31 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edu_app", "0012_remove_stu_attendance_is_present_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stu_attendance",
            name="attendance",
            field=models.CharField(default="Absent", max_length=10),
        ),
        migrations.AlterField(
            model_name="stu_attendance",
            name="date",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AlterField(
            model_name="stu_attendance",
            name="ending_time",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AlterField(
            model_name="stu_attendance",
            name="starting_time",
            field=models.CharField(default="", max_length=10),
        ),
    ]
