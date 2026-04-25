import os
import requests
from django.utils import timezone
from datetime import datetime
from .models import Pesquisa, Noticia, AnaliseSentimento, ResumoIA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.environ.get('GNEWS_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

def fetch_news_from_gnews(query: str):
    """
    Busca notícias recentes sobre o termo usando a GNews API.
    """
    pesquisa, created = Pesquisa.objects.get_or_create(termo=query.lower())
    
    url = f"https://gnews.io/api/v4/search?q={query}&lang=pt&country=br&max=10&apikey={GNEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('articles', [])
        
        for article in articles:
            # Converter a string ISO para datetime
            pub_date_str = article.get('publishedAt')
            try:
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                pub_date = timezone.now()
                
            noticia, not_created = Noticia.objects.get_or_create(
                url=article.get('url'),
                defaults={
                    'pesquisa': pesquisa,
                    'titulo': article.get('title', '')[:500],
                    'resumo': article.get('description', ''),
                    'data_publicacao': pub_date
                }
            )
            
            # Se a noticia for nova, já cria a análise de sentimento inicial
            if not_created:
                analyze_news_sentiment(noticia)
                
        return pesquisa
    except Exception as e:
        print(f"Erro ao buscar notícias: {e}")
        return pesquisa

def analyze_news_sentiment(noticia: Noticia):
    """
    Análise de sentimento baseada em palavras-chave (simulando NLP rápido).
    Para produção, usaríamos modelos robustos de NLP locais ou via API.
    """
    texto = (noticia.titulo + " " + noticia.resumo).lower()
    
    palavras_positivas = [
        'sucesso', 'crescimento', 'lucro', 'inovação', 'alta', 'recorde', 'lançamento', 
        'bom', 'excelente', 'positivo', 'avanço', 'conquista', 'expansão', 'valorização',
        'supera', 'destaque', 'melhor', 'melhoria', 'otimismo', 'vitória', 'investimento',
        'parceria', 'acordo', 'solução', 'benefício', 'confiança', 'sustentável', 'vantagem',
        'lucratividade', 'aprovado', 'líder', 'liderança', 'prêmio', 'premiado', 'dispara',
        'oportunidade', 'lucros', 'promissor', 'recuperação', 'forte', 'solidez', 'seguro'
    ]
    
    palavras_negativas = [
        'crise', 'queda', 'prejuízo', 'falha', 'rebaixamento', 'ruim', 'problema', 
        'demissão', 'escândalo', 'negativo', 'recuo', 'perda', 'desvalorização', 'desaba',
        'pior', 'multa', 'processo', 'investigação', 'fraude', 'corrupção', 'polêmica',
        'denúncia', 'dívida', 'calote', 'rombo', 'atraso', 'cancelamento', 'risco',
        'instabilidade', 'fechamento', 'falência', 'corte', 'cortes', 'desemprego', 'pânico',
        'tensão', 'desastre', 'fracasso', 'preocupação', 'desaponta', 'decepção', 'lento'
    ]
    
    score = 0
    for palavra in palavras_positivas:
        if palavra in texto:
            score += 1
            
    for palavra in palavras_negativas:
        if palavra in texto:
            score -= 1
            
    classificacao = 'NEUTRO'
    if score > 0:
        classificacao = 'POSITIVO'
    elif score < 0:
        classificacao = 'NEGATIVO'
        
    AnaliseSentimento.objects.create(
        noticia=noticia,
        classificacao=classificacao,
        pontuacao=float(score)
    )

def generate_ai_summary(pesquisa: Pesquisa):
    """
    Usa o LangChain e a API do Gemini para criar um resumo das notícias e um alerta.
    """
    if not GEMINI_API_KEY:
        print("Chave do Gemini não configurada.")
        return None
        
    noticias = pesquisa.noticias.all().order_by('-data_publicacao')[:10]
    
    if not noticias.exists():
        return None
        
    contexto_noticias = ""
    for n in noticias:
        contexto_noticias += f"- Título: {n.titulo}\n  Resumo: {n.resumo}\n\n"
        
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=GEMINI_API_KEY)
    
    template = """
    Você é um assistente de Relações Públicas analisando a percepção de uma marca.
    Abaixo estão as últimas notícias sobre a marca ou tema: "{termo}".
    
    Notícias:
    {noticias}
    
    Por favor, escreva um resumo executivo de no máximo 2 parágrafos. 
    Destaque:
    1. O principal acontecimento no momento.
    2. Se a percepção atual é mais positiva, negativa ou neutra e por quê.
    Seja direto, profissional e use tom jornalístico.
    """
    
    prompt = PromptTemplate(template=template, input_variables=["termo", "noticias"])
    chain = prompt | llm | StrOutputParser()
    
    try:
        resultado = chain.invoke({"termo": pesquisa.termo, "noticias": contexto_noticias})
        
        # Limpar possiveis asteriscos e markdowns extras se o Gemini mandar
        resultado_limpo = resultado.replace('**', '').strip()
        
        resumo, created = ResumoIA.objects.update_or_create(
            pesquisa=pesquisa,
            defaults={'texto_resumo': resultado_limpo}
        )
        return resumo
    except Exception as e:
        print(f"Erro na IA: {e}")
        return None
