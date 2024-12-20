# Generated by Django 4.2.16 on 2024-10-20 04:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marketplace", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tax",
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
                ("tax_type", models.CharField(max_length=50, unique=True)),
                (
                    "tax_percentage",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="TaxPercentage(%)"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]
