# Generated by Django 5.1.3 on 2024-11-20 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("technician", "0002_repairrequest_staff_notes"),
    ]

    operations = [
        migrations.AddField(
            model_name="repairrequest",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
