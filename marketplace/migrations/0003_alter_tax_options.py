# Generated by Django 4.2.16 on 2024-10-23 07:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("marketplace", "0002_tax"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tax",
            options={"verbose_name_plural": "tax"},
        ),
    ]
