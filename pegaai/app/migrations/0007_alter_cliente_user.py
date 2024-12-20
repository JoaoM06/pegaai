# Generated by Django 5.1.2 on 2024-12-11 00:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_remove_cliente_dt_nasc_remove_cliente_email_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="cliente",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cliente",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
