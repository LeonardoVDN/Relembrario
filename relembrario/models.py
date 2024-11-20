# models.py
from django.db import models
from django.contrib.auth.models import User

class Lembrancas(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(max_length=20, null=True)
    data_evento = models.DateField(null=True, blank=True)
    local = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    imagem = models.ImageField(upload_to='imagens_lembrancas/', blank=True, null=True)
    destaque = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.titulo

class Tag(models.Model):
    nome = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Amizade(models.Model):
    solicitante = models.ForeignKey(User, related_name='amizades_iniciadas', on_delete=models.CASCADE)
    amigo = models.ForeignKey(User, related_name='amizades_recebidas', on_delete=models.CASCADE)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    aceito = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.solicitante.username} é amigo de {self.amigo.username}' if self.aceito else f'Solicitação pendente entre {self.solicitante.username} e {self.amigo.username}'
