# Generated by Django 5.1.2 on 2024-11-09 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="estabelecimento",
            name="descricao",
            field=models.TextField(blank=True),
        ),
    ]
