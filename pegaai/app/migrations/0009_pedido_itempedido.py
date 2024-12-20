# Generated by Django 5.1.2 on 2024-12-12 01:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_estabelecimento_user_alter_estabelecimento_score"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pedido",
            fields=[
                (
                    "id_pedido",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("data_pedido", models.DateTimeField(auto_now_add=True)),
                ("confirmado", models.BooleanField(default=False)),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.cliente"
                    ),
                ),
                (
                    "estabelecimento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.estabelecimento",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ItemPedido",
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
                ("quantidade", models.PositiveIntegerField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.itens"
                    ),
                ),
                (
                    "pedido",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="itens",
                        to="app.pedido",
                    ),
                ),
            ],
        ),
    ]
