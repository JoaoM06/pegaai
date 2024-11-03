from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registrar", views.register),
    path("entrar", views.login),
    path("menu", views.menu),
    path("pedidos", views.orders, name="orders"),
    path("perfil", views.profile, name="profile")
]