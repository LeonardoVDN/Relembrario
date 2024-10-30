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
