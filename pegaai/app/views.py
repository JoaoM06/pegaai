from django.shortcuts import render, redirect, get_object_or_404
from .models import Estabelecimento
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import UserRegisterForm, EstablishmentRegisterForm, EstablishmentAddForm
from django.http import JsonResponse
from .models import Itens, ItemCliente,Cliente
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

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
def orders(request):
    return render(request, "orders.html")

@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def cart(request):
    return render(request, "cart.html")

@login_required
def establishment(request):
    return render(request, "establishment.html")

def payment_info(request):
    return render(request, "payment_info.html")

def privacity(request):
    return render(request, "privacity.html")

@login_required
def account_settings(request):
    return render(request, "account_settings.html")

@login_required
# def itens_estabelecimento(request, id_estabelecimento):
#     estabelecimento = get_object_or_404(Estabelecimento, id_estabelecimento=id_estabelecimento)
#     itens = estabelecimento.itens.all()
#     return render(request, 'menu.html', {'estabelecimento': estabelecimento, 'itens': itens})
def itens_estabelecimento(request, id_estabelecimento):
    estabelecimento = get_object_or_404(Estabelecimento, id_estabelecimento=id_estabelecimento)
    itens = estabelecimento.itens.all()  # Relacionamento com os itens
    return render(request, 'establishment.html', {'estabelecimento': estabelecimento, 'itens': itens})
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
    form = EstablishmentRegisterForm()
    if request.method == 'POST' and request.POST:
        form = EstablishmentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Estabelecimento')
            user.groups.add(group)
            return redirect('/login')
    else:
        form = EstablishmentRegisterForm()
    return render(request, 'register_establishment.html', {'form': form})

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




# @login_required
# def add_to_cart(request, id_item):
#     item = get_object_or_404(Itens, id_item=id_item)
#     cliente = request.user.cliente  # Assumindo que cada usuário tem um perfil de cliente relacionado
#     estabelecimento = item.id_estabelecimento

#     # Verificar se o cliente já possui itens no carrinho de outro estabelecimento
#     existing_items = ItemCliente.objects.filter(id_cliente=cliente, id_estabelecimento__isnull=False).distinct('id_estabelecimento')
#     if existing_items.exists() and existing_items.first().id_estabelecimento != estabelecimento:
#         return JsonResponse({'error': 'Você só pode adicionar itens de um único estabelecimento ao carrinho.'}, status=400)

#     # Verificar se há estoque suficiente
#     quantidade = int(request.POST.get('quantidade', 1))
#     if item.estoque < quantidade:
#         return JsonResponse({'error': 'Estoque insuficiente para o item selecionado.'}, status=400)

#     # Adicionar ou atualizar o item no carrinho
#     cart_item, created = ItemCliente.objects.get_or_create(
#         id_cliente=cliente,
#         id_item=item,
#         id_estabelecimento=estabelecimento,
#         defaults={'dataehora': now(), 'qtd': quantidade}
#     )
#     if not created:
#         cart_item.qtd += quantidade
#         cart_item.save()

#     # Atualizar o estoque do item
#     item.estoque -= quantidade
#     item.save()

#     return JsonResponse({'message': 'Item adicionado ao carrinho com sucesso!'})

@login_required
def add_to_cart(request, id_item):
    # Tenta obter o perfil de cliente do usuário
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Usuário não possui um perfil de cliente associado.'}, status=400)

    item = get_object_or_404(Itens, id_item=id_item)
    estabelecimento = item.id_estabelecimento

    # Verificar se o cliente já possui itens no carrinho de outro estabelecimento

    # existing_items = ItemCliente.objects.filter(id_cliente=cliente, id_estabelecimento__isnull=False).distinct('id_estabelecimento')
    # if existing_items.exists() and existing_items.first().id_estabelecimento != estabelecimento:
    #     return JsonResponse({'error': 'Você só pode adicionar itens de um único estabelecimento ao carrinho.'}, status=400)
    
    existing_items = ItemCliente.objects.filter(id_cliente=cliente, id_estabelecimento__isnull=False)
    estabelecimentos = existing_items.values_list('id_estabelecimento', flat=True).distinct()

    if estabelecimentos and estabelecimentos[0] != estabelecimento.id_estabelecimento:
        return JsonResponse({
            'error': 'Você só pode adicionar itens de um único estabelecimento ao carrinho.'
        }, status=400)

    # Verificar se há estoque suficiente
    quantidade = int(request.POST.get('quantidade', 1))
    if item.estoque < quantidade:
        return JsonResponse({'error': 'Estoque insuficiente para o item selecionado.'}, status=400)

    # Adicionar ou atualizar o item no carrinho
    cart_item, created = ItemCliente.objects.get_or_create(
        id_cliente=cliente,
        id_item=item,
        id_estabelecimento=estabelecimento,
        defaults={'dataehora': now(), 'qtd': quantidade}
    )
    if not created:
        cart_item.qtd += quantidade
        cart_item.save()

    # Atualizar o estoque do item
    item.estoque -= quantidade
    item.save()

    return JsonResponse({'message': 'Item adicionado ao carrinho com sucesso!'})


@login_required
def view_cart(request):
    cliente = request.user.cliente  # Assumindo que cada usuário tem um perfil de cliente relacionado
    cart_items = ItemCliente.objects.filter(id_cliente=cliente)
    
    total = sum(item.qtd * item.id_item.valor_item for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
@login_required
def remove_from_cart(request, id_item):
    cliente = request.user.cliente
    cart_item = get_object_or_404(ItemCliente, id_cliente=cliente, id_item=id_item)
    
    # Devolver o estoque
    cart_item.id_item.estoque += cart_item.qtd
    cart_item.id_item.save()

    cart_item.delete()

    return redirect('view_cart')
@receiver(post_save, sender=User)
def criar_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)

@receiver(post_save, sender=User)
def salvar_cliente(sender, instance, **kwargs):
    instance.cliente.save()