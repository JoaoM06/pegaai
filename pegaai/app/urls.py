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
    path("cart", views.cart, name="cart"),
    path('login/',views.login_usuario,name='login'),
    path('logout/',views.logout_usuario,name='logout'),
    path('index/',views.home,name='home'),


    path('estabelecimento/<uuid:id_estabelecimento>/itens/', views.itens_estabelecimento, name='itens_estabelecimento'),
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario')
]


