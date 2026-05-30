# 🎯 Brand Tracker AI

> Sistema de monitoramento de marcas com análise de sentimento e resumos gerados por Inteligência Artificial (Google Gemini).

---

## 📋 Sobre o Projeto

O **Brand Tracker AI** é uma aplicação Django que permite rastrear como uma marca é mencionada na mídia, classificar automaticamente o sentimento das notícias (positivo, neutro ou negativo) e gerar resumos inteligentes usando a API do Google Gemini.

### Funcionalidades principais

- 🔍 **Pesquisa de marcas** — cadastro e rastreamento de termos/marcas
- 📰 **Coleta de notícias** — integração com a API GNews para buscar notícias em tempo real
- 🤖 **Análise de sentimento** — classificação automática via IA (Positivo / Neutro / Negativo)
- 📊 **Resumo IA** — geração de resumos consolidados com Google Gemini
- 🏥 **Diagnóstico de mercado** — formulário de aderência para avaliar o potencial de uso
- 🎨 **Painel Admin** — interface administrativa com tema dark (Django Jazzmin)

---

## 🛠️ Stack Tecnológica

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.13 | Linguagem principal |
| Django | 4.2.x | Framework web |
| SQLite | — | Banco de dados (dev) |
| Django Jazzmin | 3.x | Tema do painel admin |
| LangChain + Gemini | — | IA para resumos e análise |
| GNews API | — | Coleta de notícias |
| Celery + Redis | — | Tarefas assíncronas (opcional) |
| Daphne + Channels | — | Suporte a WebSocket (opcional) |

---

## ⚙️ Pré-requisitos

- **Python 3.10+** instalado e no PATH
- **pip** (gerenciador de pacotes Python)
- Chaves de API:
  - `GNEWS_API_KEY` — obtida em [gnews.io](https://gnews.io)
  - `GEMINI_API_KEY` — obtida no [Google AI Studio](https://aistudio.google.com)

> ⚠️ **Redis** só é necessário se for usar Celery (tarefas em background). Para rodar localmente no modo básico, não é necessário.

---

## 🚀 Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd "Aula 1 - Projeto 3"
```

### 2. Configure o arquivo `.env`

Edite o arquivo `.env` na raiz do projeto com suas credenciais:

```env
# Chaves de API
GNEWS_API_KEY=sua-chave-gnews-aqui
GEMINI_API_KEY=sua-chave-gemini-aqui

# Django
SECRET_KEY=uma-chave-secreta-forte-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

> 💡 Nunca compartilhe o `.env` com suas chaves reais. Adicione-o ao `.gitignore`.

### 3. Instale as dependências

> ⚠️ **Importante:** o `requirements.txt` não inclui `django-jazzmin` explicitamente. Instale manualmente:

```powershell
pip install -r requirements.txt
pip install django-jazzmin
```

### 4. Aplique as migrations

```powershell
python manage.py migrate
```

### 5. Crie um superusuário (para acessar o admin)

```powershell
python manage.py createsuperuser
```

Siga as instruções: informe usuário, e-mail e senha.

### 6. Rode o servidor

```powershell
python manage.py runserver
```

✅ O servidor estará disponível em:

| URL | Descrição |
|---|---|
| http://127.0.0.1:8000/ | Dashboard principal |
| http://127.0.0.1:8000/admin/ | Painel administrativo |

---

## 🗂️ Estrutura do Projeto

```
Aula 1 - Projeto 3/
├── backend/                  # Configurações do projeto Django
│   ├── settings.py           # Configurações gerais (DB, apps, Jazzmin, etc.)
│   ├── urls.py               # Roteamento principal
│   ├── asgi.py               # Configuração ASGI (Daphne/Channels)
│   └── wsgi.py               # Configuração WSGI
├── tracker/                  # App principal
│   ├── models.py             # Modelos: Pesquisa, Noticia, AnaliseSentimento, ResumoIA, DiagnosticoMercado
│   ├── views.py              # Views e lógica das páginas
│   ├── urls.py               # URLs do app tracker
│   ├── admin.py              # Configuração do painel admin
│   ├── services.py           # Integração com GNews e Gemini
│   ├── templates/            # Templates HTML
│   └── static/               # Arquivos estáticos (CSS, JS)
├── staticfiles/              # Arquivos estáticos coletados (produção)
├── db.sqlite3                # Banco de dados SQLite
├── manage.py                 # CLI do Django
├── requirements.txt          # Dependências Python
└── .env                      # Variáveis de ambiente (não versionar!)
```

---

## 🗃️ Modelos de Dados

```
Pesquisa          → termo rastreado (ex: "Nike", "Apple")
  └── Noticia     → artigos coletados via GNews
        └── AnaliseSentimento  → POSITIVO / NEUTRO / NEGATIVO
  └── ResumoIA    → resumo gerado pelo Google Gemini

DiagnosticoMercado → formulário de aderência (score 0–100%)
```

---

## 🐛 Problemas Conhecidos e Soluções

### ❌ `ModuleNotFoundError: No module named 'jazzmin'`

O `django-jazzmin` não está incluído no `requirements.txt` com o nome correto. Solução:

```powershell
pip install django-jazzmin
```

---

### ❌ `.\venv\Scripts\activate` não funciona no terminal

Se você estiver usando **Git Bash** ou outro shell que não seja o PowerShell nativo do Windows, o comando de ativar o venv é diferente:

| Terminal | Comando |
|---|---|
| PowerShell | `.\venv\Scripts\Activate.ps1` |
| CMD | `venv\Scripts\activate.bat` |
| Git Bash | `source venv/Scripts/activate` |

> 💡 O projeto funciona sem ativar o venv desde que os pacotes estejam instalados globalmente (como é o caso desta máquina).

---

### ❌ Erro de `ExecutionPolicy` no PowerShell

Se o PowerShell bloquear a execução de scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## 📦 Adicionando `django-jazzmin` ao requirements.txt

Para evitar o problema do módulo ausente em outros ambientes, adicione ao `requirements.txt`:

```
django-jazzmin>=3.0.0
```

---

## 🔧 Comandos Úteis

```powershell
# Verificar se o projeto está correto (sem erros de configuração)
python manage.py check

# Criar novas migrations após alterar models.py
python manage.py makemigrations

# Aplicar migrations no banco
python manage.py migrate

# Coletar arquivos estáticos (produção)
python manage.py collectstatic

# Abrir o shell interativo do Django
python manage.py shell

# Listar todas as URLs registradas
python manage.py show_urls
```

---

## 🤝 Contribuindo

1. Crie uma branch: `git checkout -b feature/minha-feature`
2. Faça suas alterações e commite: `git commit -m 'feat: minha nova feature'`
3. Envie a branch: `git push origin feature/minha-feature`
4. Abra um Pull Request

---

## 📄 Licença

Projeto acadêmico — Aula 1, Projeto III.
