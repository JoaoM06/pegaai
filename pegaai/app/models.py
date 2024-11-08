from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class estabelecimento(models.Model):
    Nome= models.CharField(max_length=255)
    Tipo= models.CharField(max_length=255)
    Score= models.DecimalField(max_digits=3, decimal_places=2,validators=[
        MinValueValidator(0.00),
        MaxValueValidator(5.00)
        ])
    CNPJ= models.CharField(max_length=18,
        primary_key=True,
        validators=[MinLengthValidator(18)])
        

class Itens(models.Model):
    id_item=models.IntegerField(primary_key=True)
    nome_item=models.CharField(max_length=255)
    valor_item=models.DecimalField(max_digits=6,decimal_places=2,validators=[
        MinValueValidator(0.00)])
    descricao=models.TextField()
    estoque=models.IntegerField(validators=[MinValueValidator(0)])
    id_estabelecimento=models.ForeignKey(estabelecimento,on_delete=models.CASCADE,related_name='CNPJ',verbose_name='ID_estabelecimento')

class Cliente(models.Model):
    CPF=models.CharField(primary_key=True,validators=[MinLengthValidator(14)])
    Nome=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    dt_nasc=models.DateField()



class Item_Cliente(models.Model):
    id_item=models.ForeignKey(Itens,on_delete=models.CASCADE,related_name='id_item',verbose_name="ID_item")
    id_cliente=models.ForeignKey(Cliente,on_delete=models.CASCADE,related_name='CPF',verbose_name='ID_cliente')
    dataehora=models.DateTimeField
    qtd=models.IntegerField(validators=[models.validators.MinValueValidator(0)])
    id_estabelecimento=models.ForeignKey(estabelecimento,on_delete=models.CASCADE,related_name='CNPJ',verbose_name='ID_estabelecimento')

