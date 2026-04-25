# Diagrama de Arquitetura do Projeto

Abaixo está o diagrama visual da arquitetura proposta para o sistema Django com Dashboard Interativo e Agente de IA.

```mermaid
flowchart TB
    %% Styling
    classDef frontend fill:#E3F2FD,stroke:#1565C0,stroke-width:2px;
    classDef backend fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px;
    classDef service fill:#FFF3E0,stroke:#E65100,stroke-width:2px;
    classDef storage fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px;
    classDef external fill:#ECEFF1,stroke:#455A64,stroke-width:2px,stroke-dasharray: 5 5;

    %% Nodes
    subgraph Frontend_Layer ["🖥️ Frontend (Interface do Usuário)"]
        UI["Dashboard & Chat\n(React/Next.js ou HTMX/Tailwind)"]:::frontend
    end

    subgraph Backend_Layer ["⚙️ Backend (Django)"]
        API["Django REST API\n(HTTP/REST)"]:::backend
        WS["Django Channels\n(WebSockets)"]:::backend
        Apps["Módulos Internos\n(Users, Dashboard, AI_Agent)"]:::backend
    end

    subgraph Async_Layer ["⚡ Processamento Assíncrono e IA"]
        Celery["Celery Workers\n(Background Jobs)"]:::service
        AI["Serviço de IA\n(LangChain/LlamaIndex)"]:::service
    end

    subgraph Data_Layer ["💾 Armazenamento e Fila"]
        Redis[("Redis\n(Fila do Celery)")]:::storage
        DB[("PostgreSQL\n(Dados Relacionais)")]:::storage
    end

    LLM(("🤖 API do LLM\n(OpenAI, Anthropic, etc.)")):::external

    %% Connections
    UI <-->|"HTTP (JSON)"| API
    UI <-->|"WebSockets (Streaming)"| WS
    
    API <--> Apps
    WS <--> Apps
    
    Apps <-->|"Leitura/Escrita"| DB
    Apps -.->|"Envia Tarefas"| Redis
    
    Redis -.->|"Consome Tarefas"| Celery
    Celery --> AI
    
    AI <-->|"Busca de Dados"| DB
    AI <-->|"Geração de Texto"| LLM
```

## Como ler o diagrama:
1. **Frontend**: O usuário interage com o dashboard e o chat, enviando requisições REST tradicionais para atualizações e WebSockets para streaming em tempo real do agente de IA.
2. **Backend**: O Django atua como o cérebro central, recebendo as solicitações. `Django Channels` gerencia a comunicação em tempo real e o `Django REST API` gerencia os endpoints CRUD.
3. **Async & IA**: Quando uma solicitação exige IA, ela é enviada para a fila (`Redis`) onde os `Celery Workers` pegam o trabalho pesado sem travar o sistema. O agente processa a lógica utilizando ferramentas como `LangChain`.
4. **Armazenamento**: O agente consulta o banco relacional (`PostgreSQL`) para obter os dados estruturados do sistema e montar o contexto.
5. **LLM**: Por fim, a requisição é formatada e enviada de forma externa para o modelo de inteligência artificial (OpenAI, Anthropic, etc.) e a resposta é devolvida ao usuário.
