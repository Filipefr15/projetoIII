from django.db import models

class Pesquisa(models.Model):
    termo = models.CharField(max_length=255, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.termo

class Noticia(models.Model):
    pesquisa = models.ForeignKey(Pesquisa, on_delete=models.CASCADE, related_name="noticias")
    titulo = models.CharField(max_length=500)
    resumo = models.TextField()
    url = models.URLField(max_length=2000, unique=True)
    data_publicacao = models.DateTimeField()
    data_coleta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class AnaliseSentimento(models.Model):
    SENTIMENTO_CHOICES = [
        ('POSITIVO', 'Positivo'),
        ('NEUTRO', 'Neutro'),
        ('NEGATIVO', 'Negativo'),
    ]
    noticia = models.OneToOneField(Noticia, on_delete=models.CASCADE, related_name="analise")
    classificacao = models.CharField(max_length=20, choices=SENTIMENTO_CHOICES)
    pontuacao = models.FloatField(default=0.0)
    data_analise = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.noticia.titulo[:50]} - {self.classificacao}"

class ResumoIA(models.Model):
    pesquisa = models.OneToOneField(Pesquisa, on_delete=models.CASCADE, related_name="resumo_ia")
    texto_resumo = models.TextField()
    data_geracao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resumo IA para: {self.pesquisa.termo}"
