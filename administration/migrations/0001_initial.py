# Generated by Django 5.1.3 on 2024-11-06 19:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Asset",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("university_barcode", models.CharField(max_length=50, unique=True)),
                ("serial_number", models.CharField(max_length=50, unique=True)),
                ("image", models.ImageField(upload_to="assets/images/")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("damaged", "Damaged"),
                            ("good condition", "Good Condition"),
                            ("fixed", "Fixed"),
                            ("missing", "Missing"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Office",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("building_name", models.CharField(max_length=100)),
                ("office_number", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stuff_number", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=100)),
                ("surname", models.CharField(max_length=100)),
                ("national_id", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "passport_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("not active", "Not Active")],
                        max_length=10,
                    ),
                ),
                (
                    "office",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="administration.office",
                    ),
                ),
            ],
        ),
    ]