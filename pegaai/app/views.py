from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import UserRegisterForm, EstablishmentRegisterForm, EstablishmentAddForm
from django.http import JsonResponse
from .models import Itens, ItemCliente, Cliente, Estabelecimento, Pedido, ItemPedido
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib import messages

def not_logged(usuario):
    return not usuario.is_authenticated


@login_required
def home(request):
    estabelecimentos = Estabelecimento.objects.all()
    return render(request, "index.html", {"estabelecimentos": estabelecimentos})

@login_required
def menu(request):
    return render(request, "menu.html")

@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def cart(request):
    return render(request, "cart.html")

@login_required
def establishment_profile(request):
    return render(request, "establishment_profile.html")


def payment_info(request):
    return render(request, "payment_info.html")

def privacity(request):
    return render(request, "privacity.html")

@login_required
def account_settings(request):
    return render(request, "account_settings.html")

@login_required
def itens_estabelecimento(request, id_estabelecimento):
    estabelecimento = get_object_or_404(Estabelecimento, id_estabelecimento=id_estabelecimento)
    itens = estabelecimento.itens.all()
    return render(request, 'menu.html', {'estabelecimento': estabelecimento, 'itens': itens})

@user_passes_test(not_logged, login_url='/')
def register_user(request):
    return render(request, 'register.html')

@user_passes_test(not_logged, login_url='/')
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

@user_passes_test(not_logged, login_url='/')
def register_establishment(request):
    if request.method == "POST":
        form = EstablishmentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Estabelecimento registrado com sucesso!")
            return redirect("home")
    else:
        form = EstablishmentRegisterForm()

    return render(request, "register_establishment.html", {"form": form})

@user_passes_test(not_logged, login_url='/')
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
def user_logout(request):
    logout(request)
    return redirect('/')

def add_establishment(request):
    if request.method == 'POST':
        form = EstablishmentAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EstablishmentAddForm()
    
    return render(request, 'add_establishment.html', {'form': form})


def add_to_cart(request, id_item):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        return render(request, 'menu.html', {
            'error_message': 'Usuário não possui um perfil de cliente associado.'
        })

    item = get_object_or_404(Itens, id_item=id_item)
    estabelecimento = item.id_estabelecimento

    existing_items = ItemCliente.objects.filter(id_cliente=cliente, id_estabelecimento__isnull=False)
    estabelecimentos = existing_items.values_list('id_estabelecimento', flat=True).distinct()

    if estabelecimentos and estabelecimentos[0] != estabelecimento.id_estabelecimento:
        itens = Itens.objects.filter(id_estabelecimento=estabelecimento)
        return render(request, 'menu.html', {
            'itens': itens,
            'error_message': 'Você só pode adicionar itens de um único estabelecimento ao carrinho.'
        })

    quantidade = int(request.POST.get('quantidade', 1))
    if item.estoque < quantidade:
        itens = Itens.objects.filter(id_estabelecimento=estabelecimento)
        return render(request, 'menu.html', {
            'itens': itens,
            'error_message': 'Estoque insuficiente para o item selecionado.'
        })

    cart_item, created = ItemCliente.objects.get_or_create(
        id_cliente=cliente,
        id_item=item,
        id_estabelecimento=estabelecimento,
        defaults={'dataehora': now(), 'qtd': quantidade}
    )
    if not created:
        cart_item.qtd += quantidade
        cart_item.save()

    item.estoque -= quantidade
    item.save()

    itens = Itens.objects.filter(id_estabelecimento=estabelecimento)
    return render(request, 'menu.html', {
        'itens': itens,
        'success_message': 'Item adicionado ao carrinho com sucesso!'
    })

@login_required
def view_cart(request):
    cliente = request.user.cliente
    cart_items = ItemCliente.objects.filter(id_cliente=cliente)
    
    total = sum(item.qtd * item.id_item.valor_item for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def add_cart_item(request, id_item):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.error(request, 'Usuário não possui um perfil de cliente associado.')
        return redirect('itens_estabelecimento')

    item = get_object_or_404(Itens, pk=id_item)
    cart_item, created = ItemCliente.objects.get_or_create(id_cliente=cliente, id_item=item)

    if created:
        messages.success(request, f'Item {item.nome_item} adicionado ao carrinho.')
    else:
        if cart_item.qtd < item.estoque:
            cart_item.qtd += 1
            cart_item.save()
        else:
            messages.error(request, 'Quantidade máxima do item atingida.')

    return redirect('view_cart')

@login_required
def remove_from_cart(request, id_item):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.error(request, 'Usuário não possui um perfil de cliente associado.')
        return redirect('itens_estabelecimento')

    cart_item = ItemCliente.objects.filter(id_cliente=cliente, id_item_id=id_item).first()

    if not cart_item:
        messages.error(request, 'Item não encontrado no carrinho.')
        return redirect('view_cart')

    if cart_item.qtd > 1:
        cart_item.qtd -= 1
        cart_item.save()

    else:
        cart_item.delete()

    return redirect('view_cart')

@login_required
def checkout(request):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.error(request, "Usuário não possui um perfil de cliente associado.")
        return redirect("cart")

    itens_carrinho = ItemCliente.objects.filter(id_cliente=cliente)
    if not itens_carrinho.exists():
        messages.error(request, "Seu carrinho está vazio.")
        return redirect("cart")
    
    estabelecimento = itens_carrinho.first().id_estabelecimento
    pedido = Pedido.objects.create(cliente=cliente, estabelecimento=estabelecimento)

    for item in itens_carrinho:
        ItemPedido.objects.create(
            pedido=pedido,
            item=item.id_item,
            quantidade=item.qtd
        )
        item.delete()

    messages.success(request, "Pedido realizado com sucesso!")
    return redirect("view_cart")

@login_required
def pedidos_estabelecimento(request):
    try:
        estabelecimento = request.user.estabelecimento
    except Estabelecimento.DoesNotExist:
        messages.error(request, "Acesso negado.")
        return redirect("home")

    pedidos = Pedido.objects.filter(estabelecimento=estabelecimento, confirmado=False)
    pedidos_andamento = Pedido.objects.filter(estabelecimento=estabelecimento, confirmado=True, concluido=False)

    return render(request, "establishment_orders.html", {"pedidos": pedidos, "pedidos_andamento": pedidos_andamento})

@login_required
def confirmar_pedido(request, id_pedido):
    try:
        estabelecimento = request.user.estabelecimento
    except Estabelecimento.DoesNotExist:
        messages.error(request, "Acesso negado.")
        return redirect("home")

    pedido = get_object_or_404(Pedido, id_pedido=id_pedido, estabelecimento=estabelecimento)
    pedido.confirmado = True
    pedido.save()

    messages.success(request, "Pedido confirmado com sucesso!")
    return redirect("pedidos_estabelecimento")

@login_required
def listar_pedidos(request):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.error(request, "Usuário não possui um perfil de cliente associado.")
        return redirect("home")
    
    pedidos_confirmados = Pedido.objects.filter(cliente=cliente, confirmado=True, concluido=False).order_by("-data_pedido")
    pedidos_pendentes = Pedido.objects.filter(cliente=cliente, confirmado=False).order_by("-data_pedido")
    
    return render(request, "orders.html", {
        "pedidos_confirmados": pedidos_confirmados,
        "pedidos_pendentes": pedidos_pendentes,
    })

@login_required
def concluir_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)

    if pedido.cliente.user != request.user:
        messages.error(request, "Você não tem permissão para concluir este pedido.")
        return redirect("orders")

    pedido.concluido = True
    pedido.save()

    messages.success(request, "Pedido concluído com sucesso!")
    return redirect("orders")

@login_required
def home_estabelecimento(request):
    try:
        estabelecimento = request.user.estabelecimento
    except Estabelecimento.DoesNotExist:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("home")

    return render(request, "establishment.html", {"estabelecimento": estabelecimento})
