from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("registrar", views.register),
    path("entrar", views.login),
    path("menu", views.menu),
    path("pedidos", views.orders),
    path("perfil", views.profile)
]