# RELATO_IA.md

## Ferramentas de IA utilizadas

* ChatGPT

###  Onde a IA foi usada

* Estrutura inicial do projeto FastAPI
* Implementação de idempotência
* Lógica de retry com backoff
* Organização de pastas (services, repositories, schemas)
* Escrita de testes com pytest
* Configuração de logs estruturados
* Ajustes de erros com mypy e ruff

---

## Prompts utilizados (reais)

### Prompt 1

> "Me explique como implementar idempotência em uma API FastAPI usando PostgreSQL"

---

### Prompt 2

> "Como fazer retry com backoff em processamento assíncrono com BackgroundTasks no FastAPI?"

---

### Prompt 3

> "Me ajude a estruturar um projeto FastAPI com repository, service e schema separadamente"

---

### Prompt 4

> "Como escrever testes com pytest usando TestClient para endpoints com idempotência?"

---

## Exemplo de sugestão da IA que foi modificada/rejeitada

A IA inicialmente sugeriu utilizar uma fila externa (Celery + RabbitMQ) para processamento assíncrono.

Rejeitei essa abordagem porque aumentaria a complexidade do projeto, não era requisito do desafio e o objetivo era demonstrar uso de BackgroundTasks e simplicidade arquitetural

Em vez disso, adotei BackgroundTasks do FastAPI.

---

## Trecho 100% autoral (sem IA)

Arquivo: app/services/event_processor.py

Linhas aproximadas: 23-82


Arquivo: docker-compose.yml
Todas as linhas

arquivo main.py
Todas as linhas

## Reflexão final 

O uso de IA acelerou significativamente a construção da estrutura do projeto, especialmente na definição da arquitetura, padrões de pastas e implementação de lógica assíncrona. Por outro lado, em alguns momentos a IA sugeriu soluções mais complexas do que o necessário (como uso de filas externas), exigindo análise crítica para adequar ao escopo do desafio.
