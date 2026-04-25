# Plano de Implementação: Monitor de Marcas e Notícias (Brand Tracker)

Este documento detalha o plano de desenvolvimento do **Brand Tracker**, um sistema onde o usuário pesquisa por uma marca ou tema, e o sistema varre as notícias recentes, analisa o sentimento, gera resumos com IA e apresenta tudo em um Dashboard interativo.

## 🎯 Objetivo
Criar uma aplicação web escalável capaz de consumir APIs de notícias externas de forma assíncrona, aplicar processamento de Linguagem Natural (NLP) e Inteligência Artificial para gerar insights em tempo real sobre a percepção pública de uma marca.

---

## 🏗️ Stack Tecnológica Definida
- **Backend:** Python + Django (Core do sistema)
- **Assíncrono & Fila:** Celery + Redis
- **Banco de Dados:** PostgreSQL
- **Integração de IA:** LangChain + API Gratuita (Groq API, Gemini API ou Ollama local)
- **Fonte de Dados (News):** GNews API ou NewsAPI (Plano gratuito para desenvolvimento)
- **Comunicação em Tempo Real:** Django Channels (WebSockets)
- **Frontend / Dashboard:** *(Pendente de definição - Ver Perguntas em Aberto)*

---

## 🛠️ Requisitos Mínimos de Instalação
Para que o projeto funcione no ambiente de desenvolvimento local, será necessário providenciar:
- **Python 3.10+** instalado no sistema.
- **Docker** instalado (usaremos um `docker-compose.yml` para subir o PostgreSQL e o Redis facilmente).
- **Chave de API do GNews:** É obrigatório criar uma conta gratuita e obter a sua API Key acessando [https://gnews.io/dashboard](https://gnews.io/dashboard).
- **Chave de API de IA:** Obter a chave gratuita da Groq ou Google Gemini.

---

## 🛤️ Fases de Desenvolvimento

A construção do projeto será dividida em 5 fases lógicas:

### Fase 1: Setup da Infraestrutura e Modelagem (Fundação)
- Configuração do projeto Django (`backend/`).
- Configuração do Banco de Dados PostgreSQL.
- Criação dos modelos no banco (Tabelas: `Pesquisa`, `Noticia`, `AnaliseSentimento`, `ResumoIA`).
- Criação da estrutura base do frontend.

### Fase 2: O Motor de Busca e Filas (Backend Assíncrono)
- Configuração do Redis e do Celery.
- Criação do serviço que se conecta à API de notícias (ex: buscar as 100 notícias mais recentes sobre o termo).
- Criação do "Celery Worker" (A "caixa" do nosso diagrama que pega a requisição pesada e roda em background).

### Fase 3: Inteligência e Processamento (A Mágica da IA)
- Implementação de um classificador de sentimento básico para cada notícia (Positivo, Neutro, Negativo).
- Integração do **LangChain** com a **API Gratuita (ex: Groq para velocidade extrema ou Gemini)**.
- Criação da "Task" que pega as notícias processadas e pede à IA para gerar um "Resumo Executivo / Alerta de Crise".
- Salvamento dos resultados no PostgreSQL.

### Fase 4: O Dashboard (Interface Visual)
- Criação das views (APIs ou Templates) para entregar os dados consolidados.
- Integração de uma biblioteca de gráficos (ex: Chart.js ou ApexCharts).
- Montagem da tela contendo: Gráfico de volume de notícias por dia, Gráfico de Pizza de sentimento e o Card de Resumo da IA.

### Fase 5: O Agente Interativo (Chat com WebSockets)
- Configuração do Django Channels.
- Criação do chat lateral no Dashboard.
- O Agente de IA recebe acesso ao banco de dados das notícias para responder perguntas específicas do usuário em tempo real usando streaming de texto.

---

> [!IMPORTANT]  
> ## User Review Required
> 
> Antes de começarmos a codificar a Fase 1 (onde vou gerar toda a estrutura de pastas do Django e arquivos iniciais), preciso que você analise as perguntas abaixo. Suas respostas vão definir como vamos escrever o código.

## ❓ Open Questions (Perguntas em Aberto)

1. **Abordagem do Frontend (Muito Importante):** 
   - **Opção A (Simples e Rápido):** Usar o próprio sistema de templates do Django, misturado com HTMX e Tailwind CSS. É excelente para dashboards, você só precisa programar em Python e HTML.
   - **Opção B (Moderna e Desacoplada):** Criar uma API REST no Django e construir o Frontend separado em React/Next.js. Demanda mais código e configuração, mas é o padrão de grandes empresas de software. 
   *(Qual você prefere?)*

2. **Chaves de API (100% Gratuitas):**
   - Como o foco é custo zero para desenvolvimento, usaremos serviços com excelentes planos gratuitos. Você precisará gerar duas chaves (basta criar a conta gratuita): Uma da **Groq** ou **Gemini** (para a IA) e uma da **GNews** (para as notícias). Você tem familiaridade em gerar essas chaves quando precisarmos testar?

3. **Início Imediato:**
   - Com essas respostas alinhadas, podemos prosseguir com a execução da Fase 1 criando o projeto Django na sua pasta vazia?
