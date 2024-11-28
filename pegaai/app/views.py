from django.shortcuts import render, redirect, get_object_or_404
from .models import Estabelecimento
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import UserRegisterForm, EstablishmentRegisterForm, EstablishmentAddForm

def not_logged(usuario):
    return not usuario.is_authenticated


@login_required
def home(request):
    estabelecimentos = Estabelecimento.objects.all()
    return render(request, "index.html", {"estabelecimentos": estabelecimentos})

@login_required
def menu(request):
    return render(request, "menu.html")

@login_required
def orders(request):
    return render(request, "orders.html")

@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def cart(request):
    return render(request, "cart.html")

@login_required
def establishment(request):
    return render(request, "establishment.html")

def payment_info(request):
    return render(request, "payment_info.html")

def privacity(request):
    return render(request, "privacity.html")

@login_required
def account_settings(request):
    return render(request, "account_settings.html")

@login_required
def itens_estabelecimento(request, id_estabelecimento):
    estabelecimento = get_object_or_404(Estabelecimento, id_estabelecimento=id_estabelecimento)
    itens = estabelecimento.itens.all()
    return render(request, 'menu.html', {'estabelecimento': estabelecimento, 'itens': itens})

@user_passes_test(not_logged, login_url='/')
def register_user(request):
    return render(request, 'register.html')

@user_passes_test(not_logged, login_url='/')
def register_email(request):
    form = UserRegisterForm()
    if request.method == 'POST' and request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserRegisterForm()
    return render(request, 'register_email.html', {'form': form})

@user_passes_test(not_logged, login_url='/')
def register_establishment(request):
    form = EstablishmentRegisterForm()
    if request.method == 'POST' and request.POST:
        form = EstablishmentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Estabelecimento')
            user.groups.add(group)
            return redirect('/login')
    else:
        form = EstablishmentRegisterForm()
    return render(request, 'register_establishment.html', {'form': form})

@user_passes_test(not_logged, login_url='/')
def login_user(request):
    form=AuthenticationForm()
    if request.method == 'POST':
        form=AuthenticationForm(request, request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return redirect('/index')
    else:
        form = AuthenticationForm()
    return render(request,'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

def add_establishment(request):
    if request.method == 'POST':
        form = EstablishmentAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EstablishmentAddForm()
    
    return render(request, 'add_establishment.html', {'form': form})
