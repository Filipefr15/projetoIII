from django.contrib import admin
from .models import Pesquisa, Noticia, AnaliseSentimento, ResumoIA

@admin.register(Pesquisa)
class PesquisaAdmin(admin.ModelAdmin):
    list_display = ('termo', 'data_criacao', 'ultima_atualizacao')
    search_fields = ('termo',)
    list_filter = ('data_criacao',)

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'pesquisa', 'data_publicacao', 'data_coleta')
    search_fields = ('titulo', 'resumo', 'url')
    list_filter = ('pesquisa', 'data_publicacao')
    readonly_fields = ('data_coleta',)

@admin.register(AnaliseSentimento)
class AnaliseSentimentoAdmin(admin.ModelAdmin):
    list_display = ('noticia', 'classificacao', 'pontuacao', 'data_analise')
    list_filter = ('classificacao', 'data_analise')
    search_fields = ('noticia__titulo',)

@admin.register(ResumoIA)
class ResumoIAAdmin(admin.ModelAdmin):
    list_display = ('pesquisa', 'data_geracao')
    search_fields = ('texto_resumo', 'pesquisa__termo')
