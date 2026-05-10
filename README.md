# API de Foco e Produtividade

API backend em Python com FastAPI para registrar sessões de foco e gerar diagnóstico inteligente de produtividade.

## Contexto do desafio

O objetivo deste desafio é criar um Log de Performance que permita entender o nível de foco do usuário durante atividades de estudo, trabalho ou desenvolvimento. A API registra blocos de foco e gera um diagnóstico baseado nas métricas coletadas.

## Requisitos atendidos

- Python 3.x
- FastAPI
- SQLite
- POST /registro-foco
- GET /diagnostico-produtividade
- Validação de dados inválidos
- README explicativo
- Testes automatizados
- Transparência sobre uso de IA

## Tecnologias utilizadas

- Python
- FastAPI
- Pydantic
- SQLite
- Uvicorn
- Pytest
- HTTPX
- ChatGPT
- GitHub Copilot

## Estrutura de pastas

```text
log-performance-api/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── schemas.py
│   └── services.py
├── tests/
│   └── test_api.py
├── AI_TRANSPARENCIA.md
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml
```

## Como rodar o projeto

### 1. Criar ambiente virtual

No Windows:

```powershell
cd C:\Users\User\Documents\log-performance-api
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 3. Executar a API

```powershell
uvicorn app.main:app --reload
```

### 4. Acessar a documentação

Abra no navegador:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### GET /

Verifica se a API está online e disponível.

Resposta esperada:

```json
{
  "status": "online",
  "docs": "/docs",
  "mensagem": "API de Foco e Produtividade em execução."
}
```

### POST /registro-foco

Registra uma sessão de foco com nível de atenção, duração e comentário.

Exemplo de JSON:

```json
{
  "nivel_foco": 5,
  "tempo_minutos": 90,
  "comentario": "Estudei FastAPI e finalizei o endpoint principal sem distrações.",
  "categoria": "estudo",
  "tags": ["python", "api", "backend"]
}
```

Resposta esperada:

```json
{
  "id": 1,
  "nivel_foco": 5,
  "tempo_minutos": 90,
  "comentario": "Estudei FastAPI e finalizei o endpoint principal sem distrações.",
  "categoria": "estudo",
  "tags": ["python", "api", "backend"],
  "data_registro": "2026-05-10T15:00:00.000000+00:00"
}
```

Validações:

- `nivel_foco` entre 1 e 5.
- `tempo_minutos` maior que 0.
- `comentario` obrigatório e não vazio.
- `categoria` opcional e validada conforme o código atual.
- `tags` opcionais.

### GET /diagnostico-produtividade

Gera um diagnóstico de produtividade com base em todos os registros salvos.

Exemplo de resposta:

```json
{
  "total_registros": 2,
  "media_nivel_foco": 4.0,
  "tempo_total_focado": 120,
  "tempo_total_formatado": "2h 0min",
  "percentual_sessoes_flow": 50.0,
  "categoria_mais_produtiva": "coding",
  "mensagem_feedback": "Ótimo nível de foco! Continue mantendo o ritmo com pausas saudáveis e proteção dos seus blocos.",
  "insight_comentarios": "O WhatsApp apareceu como possível distração. Silenciar notificações pode ajudar."
}
```

Campos retornados:

- `total_registros`: número total de sessões registradas.
- `media_nivel_foco`: média do nível de foco entre todos os registros.
- `tempo_total_focado`: soma de todos os minutos de foco registrados.
- `tempo_total_formatado`: tempo total em formato `Xh Ymin`.
- `percentual_sessoes_flow`: porcentagem de sessões com foco alto (nível 4 ou 5).
- `categoria_mais_produtiva`: categoria com melhor equilíbrio entre foco médio e tempo investido.
- `mensagem_feedback`: feedback automático baseado nas métricas de produtividade.
- `insight_comentarios`: insight opcional extraído de palavras-chave nos comentários.

## Tratamento de erros

A API retorna erro `422 Unprocessable Entity` para entradas inválidas.

Exemplo de JSON inválido:

```json
{
  "nivel_foco": 7,
  "tempo_minutos": 0,
  "comentario": "",
  "categoria": "",
  "tags": []
}
```

Esse tipo de entrada é rejeitado porque:

- `nivel_foco` não está entre 1 e 5.
- `tempo_minutos` não é maior que 0.
- `comentario` está vazio.
- `categoria`, quando presente, é validada no código.

## Testes automatizados

Comando executado:

```powershell
python -m pytest -v
```

Resultado obtido:

```text
6 passed in 0.68s
```

Cenários testados:

- criação de registro válido
- rejeição de nível de foco inválido
- rejeição de comentário vazio
- rejeição de tempo inválido
- diagnóstico com registros
- diagnóstico sem registros

## Testes manuais realizados

Os testes manuais foram feitos usando a interface `/docs`.

Verificações realizadas:

- teste do GET `/`
- teste do POST `/registro-foco` com JSON válido
- teste do GET `/diagnostico-produtividade`
- teste do POST `/registro-foco` com JSON inválido
- validação do erro `422`

## Diferenciais implementados

- Persistência com SQLite.
- Campo `categoria` para classificar sessões.
- Campo `tags` para organização adicional.
- Data automática de registro.
- Tempo total formatado em horas e minutos.
- Percentual de sessões em flow.
- Categoria mais produtiva calculada.
- Identificação simples de distrações nos comentários.
- Documentação interativa em `/docs`.
- Testes automatizados.

## Transparência sobre uso de IA

O desafio permitia uso de IA e este projeto utilizou:

- ChatGPT
- GitHub Copilot no VSCode

A IA ajudou em:

- estruturação inicial
- organização de pastas
- revisão dos endpoints
- melhoria do README
- criação de testes
- validações
- comandos Git
- revisão final

A validação final foi feita manualmente pelo desenvolvedor com execução local, testes na interface `/docs` e `pytest`.

## Entrega

Fork do projeto:

https://github.com/Jbrr2021/teste-tecnico-python-backend
