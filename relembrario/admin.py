from django.contrib import admin
from relembrario.models import Lembrancas, Tag

class LembrancaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_evento', 'local', 'usuario', 'destaque')  # Campos que serão exibidos na lista
    list_display_links = ('titulo',)  # Links clicáveis para editar o registro
    list_per_page = 20  # Paginação
    search_fields = ('titulo', 'local', 'usuario__username')  # Campos que podem ser pesquisados
    list_filter = ('destaque', 'data_evento', 'usuario')  # Filtros laterais no admin

admin.site.register(Lembrancas, LembrancaAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('nome',)  # Exibe o nome da tag
    list_display_links = ('nome',)  # Torna o nome clicável
    search_fields = ('nome',)  # Campo de pesquisa para tags

admin.site.register(Tag, TagAdmin)
