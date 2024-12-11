# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User

# @receiver(post_save, sender=User)
# def criar_cliente(sender, instance, created, **kwargs):
#     """
#     Cria automaticamente um perfil de Cliente quando um novo User é criado.
#     """
#     if created:
#         from .models import Cliente  # Importação tardia para evitar circular import
#         Cliente.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def salvar_cliente(sender, instance, **kwargs):
#     """
#     Garante que o perfil de Cliente seja salvo quando o User é salvo.
#     """
#     from .models import Cliente  # Importação tardia para evitar circular import
#     if hasattr(instance, 'cliente'):
#         instance.cliente.save()
