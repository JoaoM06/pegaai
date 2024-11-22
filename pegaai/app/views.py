from django.shortcuts import render, get_object_or_404
from .models import Estabelecimento
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .forms import NovoUsuarioForm


def home(request):
    estabelecimentos = Estabelecimento.objects.all()

    return render(request, "index.html", {"estabelecimentos": estabelecimentos})

def register(request):
    return render(request, "register.html")

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

def login_usuario(request):
    formulario=AuthenticationForm()
    if request.method == 'POST':
        formulario=AuthenticationForm(request, request.POST)
        if formulario.is_valid():
            usuario=formulario.get_user()
            login(request, usuario)
            return redirect('/index')
        return render(request,'login.html', {'formulario': formulario})

def cadastro_usuario(request):
    formulario = NovoUsuarioForm()
    if request.method == 'POST' and request.POST:
        formulario = NovoUsuarioForm(request.POST)
        if formulario.is_valid():
            novo_usuario= formulario.save(commit=False)
            novo_usuario.email= formulario.cleaned_data['email']
            novo_usuario.first_name = formulario.cleaned_data['first_name']
            novo_usuario.last_name = formulario.cleaned_data['last_name']
            novo_usuario.save()
            return redirect('/login')
        return render(request,'cadastro_usuario.html',{'formulario':formulario})


@login_required 
def logout_usuario(request):
    logout(request)
    return redirect ('/')


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
