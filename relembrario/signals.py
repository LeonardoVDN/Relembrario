# relembrario/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Lembrancas

@receiver(post_delete, sender=Lembrancas)
def deletar_imagem_lembranca(sender, instance, **kwargs):
    print(f"Signal recebido para exclusão da imagem da Lembranca ID {instance.id}")
    if instance.imagem:
        print(f"Excluindo imagem: {instance.imagem.path}")
        instance.imagem.delete(save=False)
    else:
        print("Nenhuma imagem para excluir.")
