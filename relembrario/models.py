from django.db import models
from django.contrib.auth.models import User

class Lembrancas(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)  # Uma descrição detalhada da lembrança
    data_criacao = models.DateTimeField(max_length=20, null=True)  # Data em que a lembrança foi criada
    data_evento = models.DateField(null=True, blank=True)  # Data do evento relacionado à lembrança
    local = models.CharField(max_length=255, blank=True, null=True)  # Local onde a lembrança ocorreu
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Assumindo que o usuário com ID 1 é o admin
  # Relaciona a lembrança ao usuário que a criou
    imagem = models.ImageField(upload_to='imagens_lembrancas/', blank=True, null=True)  # Permite ao usuário anexar uma imagem relacionada
    destaque = models.BooleanField(default=False)  # Indica se a lembrança é destacada entre as demais
    tags = models.ManyToManyField('Tag', blank=True)  # Permite associar tags ou categorias à lembrança

    def __str__(self):
        return self.titulo

class Tag(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome