from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("menu", views.menu),
    path("pedidos", views.orders, name="orders"),
    path("orders", views.orders, name="orders"),
    path("perfil", views.profile, name="profile"),
    path("profile", views.profile, name="profile"),
    path("cart", views.cart, name="cart"),
    path('index/', views.home, name='home'),

    path('estabelecimento/<uuid:id_estabelecimento>/itens/', views.itens_estabelecimento, name='itens_estabelecimento'),

    path('register/', views.register, name='register'),
    path("register-email", views.register_email, name='register_email'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout, name='logout'),
]


