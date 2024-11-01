from django.shortcuts import render

def home(request):
    return render(request, "index.html")

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
