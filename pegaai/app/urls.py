from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registrar", views.register),
    path("register", views.register),
    path("entrar", views.login),
    path("login", views.login),
    path("menu", views.menu),
    path("pedidos", views.orders, name="orders"),
    path("orders", views.orders, name="orders"),
    path("perfil", views.profile, name="profile"),
    path("profile", views.profile, name="profile"),

     path('estabelecimento/<uuid:id_estabelecimento>/itens/', views.itens_estabelecimento, name='itens_estabelecimento'),
]