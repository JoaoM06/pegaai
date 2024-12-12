from django import forms    
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from validate_docbr import CNPJ
from .models import Estabelecimento, Cliente
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

    cpf = forms.CharField(
        label="CPF",
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={"class": "w-full p-3 border rounded", "placeholder": "XXX.XXX.XXX-XX"}),
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

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cliente = Cliente.objects.create(user=user, cpf=cpf)

        return user


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
    
class EstablishmentRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "w-full p-3 border rounded"}),
    )

    password2 = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput(attrs={"class": "w-full p-3 border rounded"}),
    )

    cnpj = forms.CharField(
        label="CNPJ",
        max_length=18,
        required=True,
        widget=forms.TextInput(attrs={"class": "w-full p-3 border rounded", "placeholder": "XX.XXX.XXX/XXXX-XX"}),
    )

    nome = forms.CharField(
        label="Nome do Estabelecimento",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"class": "w-full p-3 border rounded", "placeholder": "Nome do estabelecimento"}),
    )

    tipo = forms.CharField(
        label="Tipo de Estabelecimento",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"class": "w-full p-3 border rounded", "placeholder": "Ex: Restaurante, Lanchonete..."}),
    )

    descricao = forms.CharField(
        label="Descrição",
        required=False,
        widget=forms.Textarea(attrs={"class": "w-full p-3 border rounded", "placeholder": "Descrição do estabelecimento", "rows": 4}),
    )

    imagem = forms.ImageField(
        label="Imagem",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "w-full p-3 border rounded"}),
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
        super(EstablishmentRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-gray-100',
                'placeholder': field.label,
            })

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()

    #     estabelecimento = Estabelecimento.objects.create(
    #         user=user,
    #         cnpj=self.cleaned_data.get('cnpj'),
    #         nome=self.cleaned_data.get('nome'),
    #         tipo=self.cleaned_data.get('tipo'),
    #         descricao=self.cleaned_data.get('descricao'),
    #         imagem=self.cleaned_data.get('imagem'),
    #     )

    #     return user
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        group, created = Group.objects.get_or_create(name="Estabelecimento")
        user.groups.add(group)

        Estabelecimento.objects.create(
            user=user,
            cnpj=self.cleaned_data.get('cnpj'),
            nome=self.cleaned_data.get('nome'),
            tipo=self.cleaned_data.get('tipo'),
            descricao=self.cleaned_data.get('descricao'),
            imagem=self.cleaned_data.get('imagem'),
        )

        return user