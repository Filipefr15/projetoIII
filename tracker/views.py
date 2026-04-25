from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Pesquisa, Noticia, DiagnosticoMercado
from .services import fetch_news_from_gnews, generate_ai_summary


# ─────────────────────────────────────────
#  DIAGNOSTICO
# ─────────────────────────────────────────

@login_required(login_url='/login/')
def diagnostico_view(request):
    if request.method == 'POST':
        nome_projeto = request.POST.get('nome_projeto')
        setor = request.POST.get('setor')
        dor_monitoramento = int(request.POST.get('dor_monitoramento', 1))
        importancia_sentimento = int(request.POST.get('importancia_sentimento', 1))
        necessidade_ia = int(request.POST.get('necessidade_ia', 1))
        frequencia_crise = int(request.POST.get('frequencia_crise', 1))
        
        diagnostico = DiagnosticoMercado.objects.create(
            usuario=request.user,
            nome_projeto=nome_projeto,
            setor=setor,
            dor_monitoramento=dor_monitoramento,
            importancia_sentimento=importancia_sentimento,
            necessidade_ia=necessidade_ia,
            frequencia_crise=frequencia_crise
        )
        
        score = diagnostico.calculate_score()
        diagnostico.save()
        
        return render(request, 'tracker/diagnostico_resultado.html', {'diagnostico': diagnostico})

    return render(request, 'tracker/diagnostico_form.html')


# ─────────────────────────────────────────
#  AUTH VIEWS
# ─────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'tracker/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not password1:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
        elif password1 != password2:
            messages.error(request, 'As senhas não coincidem.')
        elif len(password1) < 6:
            messages.error(request, 'A senha deve ter no mínimo 6 caracteres.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Esse nome de usuário já está em uso.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {username}.')
            return redirect('dashboard')

    return render(request, 'tracker/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────

@login_required(login_url='/login/')
def dashboard_view(request):
    pesquisa_obj = None
    noticias = []
    resumo_ia = None
    sentimento_stats = {'POSITIVO': 0, 'NEUTRO': 0, 'NEGATIVO': 0}
    chart_data = {'labels': [], 'data': []}

    query = request.GET.get('q', '').strip()

    if query:
        pesquisa_obj = fetch_news_from_gnews(query)

        if pesquisa_obj:
            noticias = pesquisa_obj.noticias.all().order_by('-data_publicacao')

            for noticia in noticias:
                if hasattr(noticia, 'analise'):
                    sentimento_stats[noticia.analise.classificacao] += 1

            pesquisa_obj.refresh_from_db()
            if hasattr(pesquisa_obj, 'resumo_ia') and pesquisa_obj.resumo_ia.texto_resumo:
                resumo_ia = pesquisa_obj.resumo_ia.texto_resumo

            from django.db.models import Count
            from django.db.models.functions import TruncDate

            dados_grafico = (
                noticias
                .annotate(data=TruncDate('data_publicacao'))
                .values('data')
                .annotate(total=Count('id'))
                .order_by('data')
            )
            for dado in dados_grafico:
                chart_data['labels'].append(dado['data'].strftime('%d/%m/%Y'))
                chart_data['data'].append(dado['total'])

    context = {
        'query': query,
        'pesquisa': pesquisa_obj,
        'noticias': noticias[:20],
        'sentimento_stats': sentimento_stats,
        'resumo_ia': resumo_ia,
        'chart_data': chart_data,
    }
    return render(request, 'tracker/dashboard.html', context)


# ─────────────────────────────────────────
#  AI SUMMARY (async endpoint)
# ─────────────────────────────────────────

@login_required(login_url='/login/')
def ai_summary_view(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'error': 'Nenhuma query fornecida'}, status=400)

    pesquisa_obj = Pesquisa.objects.filter(termo=query.lower()).first()
    if not pesquisa_obj:
        return JsonResponse({'error': 'Pesquisa não encontrada'}, status=404)

    resumo = generate_ai_summary(pesquisa_obj)
    if resumo:
        return JsonResponse({'summary': resumo.texto_resumo})
    return JsonResponse({'summary': 'Não foi possível gerar um resumo.'})
