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

class DiagnosticoMercado(models.Model):
    SETOR_CHOICES = [
        ('TECH', 'Tecnologia'),
        ('RETAIL', 'Varejo'),
        ('FINANCE', 'Finanças'),
        ('AGRO', 'Agronegócio'),
        ('OTHER', 'Outro'),
    ]
    
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    nome_projeto = models.CharField(max_length=255)
    setor = models.CharField(max_length=20, choices=SETOR_CHOICES)
    
    # Perguntas de Diagnóstico (Escala 1-5)
    dor_monitoramento = models.IntegerField(help_text="O quanto o monitoramento manual de marcas é um problema?")
    importancia_sentimento = models.IntegerField(help_text="Qual a importância de saber o sentimento do público em tempo real?")
    necessidade_ia = models.IntegerField(help_text="O quanto resumos automáticos via IA agregariam valor?")
    frequencia_crise = models.IntegerField(help_text="Com que frequência a marca enfrenta crises de imagem?")
    
    score_aderencia = models.FloatField(default=0.0)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def calculate_score(self):
        # Lógica simples para calcular aderência
        total = self.dor_monitoramento + self.importancia_sentimento + self.necessidade_ia + self.frequencia_crise
        self.score_aderencia = (total / 20) * 100
        return self.score_aderencia

    def __str__(self):
        return f"Diagnóstico: {self.nome_projeto} - {self.score_aderencia}%"

