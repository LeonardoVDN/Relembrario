# relembrario/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Lembrancas, Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Verifica se o usuário tem um perfil associado
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            # Cria um perfil se não existir
            Profile.objects.create(user=instance)

@receiver(post_delete, sender=Lembrancas)
def deletar_imagem_lembranca(sender, instance, **kwargs):
    print(f"Signal recebido para exclusão da imagem da Lembranca ID {instance.id}")
    if instance.imagem:
        print(f"Excluindo imagem: {instance.imagem.path}")
        instance.imagem.delete(save=False)
    else:
        print("Nenhuma imagem para excluir.")
