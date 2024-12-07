import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.contrib.auth.models import User
class Estabelecimento(models.Model):
    usuario=models.ForeignKey(User,on_delete=models.CASCADE)
    id_estabelecimento = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    score = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00),
            MaxValueValidator(5.00)
        ]
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        validators=[MinLengthValidator(18)]
    )
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Itens(models.Model):
    id_item = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_item = models.CharField(max_length=255)
    valor_item = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )
    descricao = models.TextField()
    estoque = models.IntegerField(validators=[MinValueValidator(0)])
    id_estabelecimento = models.ForeignKey(
        Estabelecimento,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='id_estabelecimento'
    )

    def __str__(self):
        return self.nome_item

class Cliente(models.Model):
    usuario=models.ForeignKey(User,on_delete=models.CASCADE)
    
    id_cliente = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf = models.CharField(
        max_length=14,
        validators=[MinLengthValidator(14)]
    )
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    dt_nasc = models.DateField()

    def __str__(self):
        return self.nome

class ItemCliente(models.Model):
    id_item = models.ForeignKey(
        Itens,
        on_delete=models.CASCADE,
        related_name='item_clientes',
        verbose_name="id_item"
    )
    id_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='item_clientes',
        verbose_name='id_cliente'
    )
    dataehora = models.DateTimeField()
    qtd = models.IntegerField(validators=[MinValueValidator(0)])
    id_estabelecimento = models.ForeignKey(
        Estabelecimento,
        on_delete=models.CASCADE,
        related_name='item_clientes',
        verbose_name='id_estabelecimento'
    )


class Referencia(models.Model):
    usuario= models.ForeignKey(User,
                               on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.id_cliente} - {self.id_item}"
