from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class estabelecimento(models.Model):
    Nome= models.CharField(max_length=255)
    Tipo= models.CharField(max_length=255)
    Score= models.DecimalField(max_digits=3, Decimal_places=2,validators=[
        models.validators.MinValueValidator(0,00),
        models.validators.MaxValueValidator(5,00)
        ])
    CNPJ= models.models.CharField(max_length=18,
        unique=True,
        validators[MinLenghtValidator(18)])
        