# Generated by Django 5.1.3 on 2024-11-13 12:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("administration", "0003_alter_staff_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="staff",
            old_name="stuff_number",
            new_name="staff_number",
        ),
    ]
