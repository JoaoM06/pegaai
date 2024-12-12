# Generated by Django 5.1.2 on 2024-11-09 22:46

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "id_cliente",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "cpf",
                    models.CharField(
                        max_length=14,
                        validators=[django.core.validators.MinLengthValidator(14)],
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=100)),
                ("dt_nasc", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Estabelecimento",
            fields=[
                (
                    "id_estabelecimento",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("nome", models.CharField(max_length=255)),
                ("tipo", models.CharField(max_length=255)),
                (
                    "score",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(5.0),
                        ],
                    ),
                ),
                (
                    "cnpj",
                    models.CharField(
                        max_length=18,
                        unique=True,
                        validators=[django.core.validators.MinLengthValidator(18)],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Itens",
            fields=[
                (
                    "id_item",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("nome_item", models.CharField(max_length=255)),
                (
                    "valor_item",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=6,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("descricao", models.TextField()),
                (
                    "estoque",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "id_estabelecimento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="itens",
                        to="app.estabelecimento",
                        verbose_name="id_estabelecimento",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ItemCliente",
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
                ("dataehora", models.DateTimeField()),
                (
                    "qtd",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "id_cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item_clientes",
                        to="app.cliente",
                        verbose_name="id_cliente",
                    ),
                ),
                (
                    "id_estabelecimento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item_clientes",
                        to="app.estabelecimento",
                        verbose_name="id_estabelecimento",
                    ),
                ),
                (
                    "id_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item_clientes",
                        to="app.itens",
                        verbose_name="id_item",
                    ),
                ),
            ],
        ),
    ]
