from django.shortcuts import render, redirect, get_object_or_404
from .models import Estabelecimento
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import UserRegisterForm, EstablishmentRegisterForm, EstablishmentAddForm

@login_required
def home(request):
    estabelecimentos = Estabelecimento.objects.all()

    return render(request, "index.html", {"estabelecimentos": estabelecimentos})

def register(request):
    return render(request, "register.html")

def register_email(request):
    return render(request, "register_email.html")

def login(request):
    return render(request, "login.html")

def menu(request):
    return render(request, "menu.html")

def orders(request):
    return render(request, "orders.html")

def profile(request):
    return render(request, "profile.html")

def cart(request):
    return render(request, "cart.html")

def itens_estabelecimento(request, id_estabelecimento):
    estabelecimento = get_object_or_404(Estabelecimento, id_estabelecimento=id_estabelecimento)
    itens = estabelecimento.itens.all()
    return render(request, 'menu.html', {'estabelecimento': estabelecimento, 'itens': itens})

def register_user(request):
    return render(request, 'register.html')

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
def logout(request):
    logout(request)
    return redirect ('/')

def add_establishment(request):
    if request.method == 'POST':
        form = EstablishmentAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Ajuste conforme sua URL de destino
    else:
        form = EstablishmentAddForm()
    
    return render(request, 'add_establishment.html', {'form': form})


# @login_required
# def adcionar_referencia(request):
#     formulario=ReferenciaForm()
#     if request.method == 'POST' and request.POST:
#         formulario = ReferenciaForm(request.POST)
#         if formulario.is_valid():
#             nova_referencia= formulario.save(commit=False)
#             nova_referencia.usuario= request.user
#             nova_referencia.save()
#             return redirect("/index")
#         return render(
#             request,'profile.html',{
#                 'formulario':formulario
#             }
#         )
# @login_required
# def editar_referencia(request,id):
#     referencia=get_object_or_404(referencia,id=id,usuario=request.user)
    

# @login_required
# def home(request):
#     dados=Referencia.objects.filter(usuario=request.user).all()
#     return render(request,'login.html',{'usuario': request.user,'dados':dados})
