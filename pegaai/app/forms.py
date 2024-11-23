from django import forms    
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from validate_docbr import CNPJ
from .models import Estabelecimento

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class EstablishmentRegisterForm(UserCreationForm):
    cnpj = forms.CharField(max_length=18, required=True, help_text="Digite um CNPJ válido.")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'cnpj']

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        validator = CNPJ()

        if not validator.validate(cnpj):
            raise ValidationError("CNPJ inválido. Por favor, insira um CNPJ válido.")
        
        return cnpj
    
class EstablishmentAddForm(forms.ModelForm):
    class Meta:
        model = Estabelecimento
        fields = ['nome', 'tipo', 'score', 'cnpj', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descrição do estabelecimento'}),
            'score': forms.NumberInput(attrs={'step': '0.01', 'min': '0.00', 'max': '5.00'}),
        }