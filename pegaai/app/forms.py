from django import forms    
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from validate_docbr import CNPJ
from .models import Estabelecimento
import uuid

def image_upload_to(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{extension}"
    return f"imgs/establishment/{new_filename}"




class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "w-full p-3 border rounded"}),
    )
    password2 = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput(attrs={"class": "w-full p-3 border rounded"}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'username': "Nome de usuário",
            'email': 'E-mail',
            'first_name': 'Nome',
            'last_name': 'Sobrenome'
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-gray-100',
                'placeholder': field.label,
            })

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

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nome de usuário",
        widget=forms.TextInput(attrs={"class": "w-full p-3 border rounded", "placeholder": "Nome de usuário"}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "w-full p-3 border rounded", "placeholder": "Senha"}),
    )
    
class EstablishmentAddForm(forms.ModelForm):
    class Meta:
        model = Estabelecimento
        fields = ['nome', 'tipo', 'score', 'cnpj', 'descricao', "imagem"]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descrição do estabelecimento'}),
            'score': forms.NumberInput(attrs={'step': '0.50', 'min': '0.00', 'max': '5.00'}),
        }