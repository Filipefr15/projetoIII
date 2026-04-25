# 📚 Documentação Técnica e Diagramas: Brand Tracker

Visão completa da arquitetura, fluxo de dados e casos de uso do sistema Brand Tracker.

---

## 👤 1. Diagrama de Casos de Uso (Use Case)

Mapeia as interações do usuário final com as funcionalidades do sistema e como a Inteligência Artificial e a API Externa atuam como "Atores Secundários" no processo.

```mermaid
usecaseDiagram
    actor Usuário as "Usuário (Analista)"
    actor GNews as "API de Notícias\n<<Sistema Externo>>"
    actor Gemini as "Google Gemini\n<<LLM API>>"

    package "Brand Tracker App" {
        usecase UC1 as "Pesquisar Marca/Termo"
        usecase UC2 as "Visualizar Dashboard"
        usecase UC3 as "Consultar Gráfico de Sentimento"
        usecase UC4 as "Consultar Volume Temporal"
        usecase UC5 as "Ler Resumo da IA"
        usecase UC6 as "Ler Manchetes Originais"
        
        usecase UC7 as "Coletar Notícias"
        usecase UC8 as "Analisar Sentimento (NLP)"
        usecase UC9 as "Gerar Resumo Executivo"
    }

    Usuário --> UC1
    Usuário --> UC2
    
    UC2 ..> UC3 : <<include>>
    UC2 ..> UC4 : <<include>>
    UC2 ..> UC5 : <<include>>
    UC2 ..> UC6 : <<include>>
    
    UC1 ..> UC7 : <<include>>
    UC7 --> GNews
    
    UC7 ..> UC8 : <<include>>
    UC7 ..> UC9 : <<include>>
    
    UC9 --> Gemini
```

---

## 🏗️ 2. Arquitetura Técnica do Sistema

A visão estrutural mostrando as tecnologias envolvidas, desde a interface de usuário (Frontend) até o processamento síncrono/assíncrono no Backend e armazenamento.

```mermaid
flowchart TB
    classDef frontend fill:#E3F2FD,stroke:#1565C0,stroke-width:2px;
    classDef backend fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px;
    classDef database fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px;
    classDef external fill:#ECEFF1,stroke:#455A64,stroke-width:2px,stroke-dasharray: 5 5;

    UI["Frontend (Liquid Glass UI)\nHTMX + Tailwind + Chart.js"]:::frontend
    
    subgraph Core_Backend ["Backend (Django Core)"]
        View["Django Views\n(Controlador principal)"]:::backend
        Service["Services Layer\n(Lógica de Negócios)"]:::backend
        Model["Django ORM\n(Acesso a Dados)"]:::backend
    end
    
    DB[("Banco de Dados\n(PostgreSQL / SQLite)")]:::database
    
    GNews(("GNews API\n(Busca de Manchetes)")):::external
    Gemini(("Google Gemini\n(API via LangChain)")):::external

    UI <-->|"HTTP GET /?q=marca"| View
    View <-->|"Chama processamento"| Service
    
    Service <-->|"Consulta Notícias"| GNews
    Service <-->|"Envia contexto para Resumo"| Gemini
    
    Service <-->|"Salva/Lê dados processados"| Model
    Model <-->|"Queries SQL"| DB
```

---

## ⏱️ 3. Diagrama de Sequência (Fluxo de Busca)

Demonstra o passo a passo cronológico de tudo que acontece nos bastidores quando o usuário clica no botão "Analisar".

```mermaid
sequenceDiagram
    actor U as Usuário
    participant V as Django View
    participant S as Service (fetch_news)
    participant API as GNews API
    participant IA as LangChain (Gemini)
    participant DB as Banco de Dados
    
    U->>V: 1. Busca por "Nubank" (GET /?q=nubank)
    activate V
    
    V->>S: 2. fetch_news_from_gnews("Nubank")
    activate S
    
    S->>API: 3. Request (q=nubank, lang=pt)
    activate API
    API-->>S: 4. Retorna JSON com 10 artigos
    deactivate API
    
    S->>DB: 5. Salva Notícias e Sentimento Básico
    
    S->>IA: 6. generate_ai_summary(noticias)
    activate IA
    IA-->>S: 7. Retorna Texto do Resumo Executivo
    deactivate IA
    
    S->>DB: 8. Salva ResumoIA no Banco
    
    S-->>V: 9. Retorna Objeto Pesquisa consolidado
    deactivate S
    
    V->>DB: 10. Prepara dados para os gráficos
    V-->>U: 11. Renderiza Dashboard.html com Gráficos e IA
    deactivate V
```

---

## 💾 4. Diagrama Entidade-Relacionamento (Banco de Dados)

Mostra a estrutura do banco de dados relacional (ORM do Django) que construímos para o projeto.

```mermaid
erDiagram
    PESQUISA ||--o{ NOTICIA : "possui"
    PESQUISA ||--o| RESUMO_IA : "tem um"
    NOTICIA ||--o| ANALISE_SENTIMENTO : "tem uma"

    PESQUISA {
        int id PK
        string termo "UNIQUE"
        datetime data_criacao
        datetime ultima_atualizacao
    }

    NOTICIA {
        int id PK
        int pesquisa_id FK
        string titulo
        text resumo
        string url "UNIQUE"
        datetime data_publicacao
        datetime data_coleta
    }

    ANALISE_SENTIMENTO {
        int id PK
        int noticia_id FK "OneToOne"
        string classificacao "POSITIVO, NEUTRO, NEGATIVO"
        float pontuacao
        datetime data_analise
    }

    RESUMO_IA {
        int id PK
        int pesquisa_id FK "OneToOne"
        text texto_resumo
        datetime data_geracao
    }
```
