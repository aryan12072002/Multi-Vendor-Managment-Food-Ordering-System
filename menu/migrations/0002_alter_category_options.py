# Generated by Django 4.2.16 on 2024-10-14 12:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "category", "verbose_name_plural": "categories"},
        ),
    ]
