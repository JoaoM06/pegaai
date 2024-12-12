from django.shortcuts import render, get_object_or_404
from .models import Estabelecimento

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