# Generated by Django 5.1.3 on 2024-11-20 13:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("administration", "0006_staff_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]
