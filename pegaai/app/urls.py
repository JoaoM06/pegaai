from django.urls import path
from . import views
from .forms import CustomLoginForm
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from .views import add_to_cart
from .views import view_cart
from .views import remove_from_cart
urlpatterns = [
    path("", views.home, name="home"),
    path("menu", views.menu),
    path("pedidos", views.orders, name="orders"),
    path("orders", views.orders, name="orders"),
    path("perfil", views.profile, name="profile"),
    path("profile", views.profile, name="profile"),
    path("cart", views.cart, name="cart"),
    path("carrinho", views.cart, name="cart"),
    path('index/', views.home, name='home'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('configuracoes-conta/', views.account_settings, name='account_settings'),
    path('establishment/', views.establishment, name='establishment'),
    path('estabelecimento/', views.establishment, name='establishment'),
    path('payment-info/', views.payment_info, name='payment_info'),
    path('informacoes-estabelecimento/', views.payment_info, name='payment_info'),
    path('privacity/', views.privacity, name='privacity'),
    path('privacidade/', views.privacity, name='privacity'),

    path('estabelecimento/<uuid:id_estabelecimento>/itens/', views.itens_estabelecimento, name='itens_estabelecimento'),
    path('add-establishment/', views.add_establishment, name='add_establishment'),
    path('adicionar-estabelecimento/', views.add_establishment, name='add_establishment'),

    path('register/', views.register_user, name='register'),
    path('registrar/', views.register_user, name='register'),
    path("register-email", views.register_email, name='register_email'),
    path('registrar-com-email/', views.register_user, name='register'),
    path("register-establishment", views.register_establishment, name='register_establishment'),
    path("registrar-estabelecimento", views.register_establishment, name='register_establishment'),
    path('login/', LoginView.as_view(template_name='login.html', authentication_form=CustomLoginForm), name='login'),
    path('entrar/', LoginView.as_view(template_name='login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('sair/',views.user_logout, name='logout'),
    # path('cart/', views.view_cart, name='cart'),
    path('cart/add/<uuid:id_item>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('estabelecimento/<uuid:id_estabelecimento>/itens/', views.itens_estabelecimento, name='itens_estabelecimento'),

    path('cart/remove/<uuid:id_item>/', remove_from_cart, name='remove_from_cart')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)