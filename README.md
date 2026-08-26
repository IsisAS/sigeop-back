# API (FastAPI + Postgres)

API REST construída com **FastAPI**, **SQLAlchemy 2.x**, **Postgres** e padrão de arquitetura com camadas (Router → Service → Repository → DB), além de tratamento centralizado de erros e documentação automática via **Swagger/OpenAPI**.

---

## Sumário

- [Stack](#stack)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração](#configuração)
- [Executando com Docker](#executando-com-docker)
- [Documentação Swagger](#documentação-swagger)
- [Padrão de Arquitetura](#padrão-de-arquitetura)
- [Tratamento de Erros](#tratamento-de-erros)
- [Migrations com Flyway](#migrations-com-flyway)
- [Testes](#testes)

---

## Stack

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic v2 + pydantic-settings
- SQLAlchemy 2.x
- Postgres (psycopg v3)
- Flyway (migrations - desacoplado)
- Pytest + Coverage (testes)

---

## Estrutura do Projeto

```
backend/
├── Dockerfile
├── .env                # Variáveis de ambiente
├── pyproject.toml
├── requirements.txt
├── tests/
│   ├── conftest.py              # Fixtures (db, client)
│   ├── helpers.py               # Factories e assertions reutilizáveis
│   ├── test_users.py            # Testes do módulo users
│   ├── test_errors.py           # Testes dos handlers de erro
│   └── test_deps.py             # Testes das dependências
├── coverage/
│   └── html/                    # Relatório de cobertura (gerado)
└── src/
    ├── main.py
    ├── routes/
    │   └── routes.py
    ├── core/
    │   ├── config.py
    │   ├── deps.py
    │   └── errors/
    │       ├── errors.py         # Classes de erro (RFC 7807)
    │       ├── handlers.py       # Handler global de exceções
    │       ├── http_code.py      # Catálogo de HTTP status
    │       └── messages.py       # Catálogo de mensagens
    ├── db/
    │   ├── base.py
    │   └── session.py
    ├── common/
    │   ├── repository.py         # CRUD genérico
    │   ├── router.py             # Router genérico
    │   ├── schemas.py            # Schemas base
    │   └── service.py            # Service genérico
    └── modules/
        └── users/
            ├── user_model.py
            ├── user_repository.py
            ├── user_router.py
            ├── user_schema.py
            └── user_service.py
```

---

## Configuração

### Variáveis de Ambiente (`.env`)

O arquivo `.env` fica na raiz do backend (`backend/.env`):

```env
APP_NAME=api
ENV=dev
APP_VERSION="1.0.0"
PREFIX_ROUTER="/api/1.0.0"

# IMPORTANTE: use psycopg (v3)
DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/sigeope
```

Observações:
- `PREFIX_ROUTER` **não pode** terminar com `/` (ex.: `/api/v1/` dá erro no FastAPI).
- O host do banco (`@postgres`) deve ser o **nome do service** do Postgres no `docker-compose.yml`.

---

## Executando com Docker

Os comandos Docker devem ser executados a partir da pasta `docker/` na raiz do projeto. Consulte o [README do Docker](../docker/README.md) para mais detalhes.

```bash
cd docker

# Subir stack
docker compose up -d --build

# Logs da API
docker compose logs -f api

# Parar e remover volumes (reset do banco)
docker compose down -v
```

---

## Documentação Swagger

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- ReDoc: `http://localhost:8000/redoc`

---

## Padrão de Arquitetura

### Camadas

- **Router (módulo)**: define endpoints e injeta dependências (service).
- **Service**: regras de negócio e orquestração (chama repository).
- **Repository**: acesso ao banco via SQLAlchemy (CRUD + queries específicas).
- **DB**: engine/session, Base, models.

### Router agregador

O `main.py` não inclui módulos um a um. Ele importa um agregador:

- `src/routes/routes.py` agrega os routers dos módulos
- `src/main.py` faz `include_router(api_router, prefix=PREFIX_ROUTER)`

---

## Tratamento de Erros

Erros seguem a **RFC 7807 (Problem Details)** com `Content-Type: application/problem+json`.

Nenhum `try/catch` nos services ou controllers - o handler global captura tudo a nível de requisição.

### Arquivos

| Arquivo | Responsabilidade |
|---------|-----------------|
| `errors.py` | Classes de erro (`AppError`, `NotFoundError`, `ConflictError`, etc.) |
| `handlers.py` | Handler global que captura todas as exceções |
| `http_code.py` | Catálogo de HTTP status (`http.code.conflict`) |
| `messages.py` | Catálogo de mensagens (`msg.error.not_found`) |

### Formato RFC 7807

Todas as respostas de erro seguem este formato:

```json
{
  "type": "/errors/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "UserModel(999) não encontrado.",
  "instance": "/api/1.0.0/users/999"
}
```

### Exceções Capturadas

| Exceção | HTTP | Resposta |
|---------|------|----------|
| `NotFoundError` | 404 | Recurso não encontrado |
| `ConflictError` | 409 | Conflito (ex: email duplicado) |
| `BadRequestError` | 400 | Requisição inválida |
| `UnauthorizedError` | 401 | Não autorizado |
| `ForbiddenError` | 403 | Acesso negado |
| `RequestValidationError` | 422 | Validação de campos |
| `IntegrityError` (unique) | 409 | Constraint violation |
| `SQLAlchemyError` | 500 | Erro de banco |
| `Exception` | 500 | Erro genérico |

### Debug em DEV

Quando `ENV=dev`, erros 500 incluem stacktrace:

```json
{
  "type": "/errors/internal-server-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "Erro interno inesperado.",
  "instance": "/api/1.0.0/users",
  "debug": {
    "exception": "RuntimeError",
    "message": "descrição do erro",
    "stacktrace": ["..."]
  }
}
```

Em produção (`ENV=prod`) o campo `debug` nunca aparece.

### Como Usar nos Módulos

Basta lançar a exceção em qualquer camada (service, repository, etc.):

```python
from src.core.errors.errors import ConflictError, NotFoundError

# No service
if self.repository.get_by_email(dto.email):
    raise ConflictError("Email já cadastrado.")
```

O handler global captura e retorna a resposta padronizada automaticamente.

---

## Migrations com Flyway

O Flyway controla a evolução do schema do banco **sigeop** de forma desacoplada do backend Python, usando migrations SQL puras.

As migrations ficam em `migrations/db/migration/{profile}/` na raiz do projeto (fora do backend).

### Como Funciona no Docker Compose

```
1. postgres         → Inicia e aguarda healthcheck (pg_isready)
2. flyway           → Executa migrations e finaliza
3. api              → Inicia apenas após flyway completar com sucesso
```

Isso garante que o banco esteja com o schema atualizado **antes** da API subir.

### Convenção de Nomenclatura

Usamos **timestamp** como versão para evitar conflitos:

| Parte | Descrição | Exemplo |
|-------|-----------|---------|
| Prefixo | `V` (versioned) | `V` |
| Versão | Timestamp `YYYYMMDDHHMMSS` | `20260206120000` |
| Separador | Dois underscores | `__` |
| Descrição | snake_case | `create_users_table` |
| Extensão | `.sql` | `.sql` |

### Comandos

```bash
cd docker

# Executar migrations pendentes
docker compose run --rm flyway migrate

# Ver status das migrations
docker compose run --rm flyway info

# Validar
docker compose run --rm flyway validate

# Reparar histórico após falha
docker compose run --rm flyway repair
```

### Troubleshooting

#### Migration falhou no meio

```bash
cd docker
docker compose run --rm flyway info
docker compose run --rm flyway repair
docker compose run --rm flyway migrate
```

#### Resetar banco completamente

```bash
cd docker
docker compose down -v
docker compose up -d --build
```

---

## Testes

O projeto usa **pytest** com banco SQLite in-memory (sem dependência do Postgres). Os testes rodam em um container Docker dedicado.

### Como Rodar

```bash
cd docker
docker compose --profile test run --rm test
```

O comando gera o relatório de cobertura em terminal e HTML em `coverage/html/index.html`.

### Estrutura dos Testes

```
tests/
├── conftest.py         # Fixtures globais (db, client)
├── helpers.py          # Factories e assertions reutilizáveis
├── test_users.py       # Testes do módulo users (CRUD)
├── test_errors.py      # Testes dos handlers de erro (RFC 7807)
└── test_deps.py        # Testes das dependências
```

### Helpers (`tests/helpers.py`)

Módulo com utilitários para evitar repetição nos testes.

#### Factories

Cada módulo deve ter sua Factory. Criam dados via API sem precisar montar JSONs manualmente:

```python
from tests.helpers import UserFactory

# Criar um usuário (POST + assert 201)
user = UserFactory.create(client)

# Criar com dados específicos
user = UserFactory.create(client, name="João", email="joao@test.com")

# Criar vários de uma vez
users = UserFactory.create_many(client, 5)

# Apenas gerar o dict (sem criar no banco)
data = UserFactory.build()
data = UserFactory.build(email="custom@test.com")
```

#### Assertions RFC 7807

Funções que validam a resposta completa (status, content-type, formato):

```python
from tests.helpers import (
    assert_not_found,
    assert_conflict,
    assert_validation_error,
    assert_internal_error,
    assert_problem_json,
)

# 404 - Not Found
assert_not_found(response)

# 409 - Conflict
assert_conflict(response)

# 422 - Validation Error (com campos esperados)
assert_validation_error(response, fields=["body.name", "body.email"])

# 500 - Internal Server Error (com debug em dev)
assert_internal_error(response)

# Genérico (qualquer erro RFC 7807)
assert_problem_json(response, status=403, error_type="/errors/forbidden")
```

Cada assert valida automaticamente:
- Status code HTTP
- Header `Content-Type: application/problem+json`
- Campos obrigatórios: `type`, `title`, `status`, `detail`, `instance`

### Fixtures (`tests/conftest.py`)

| Fixture | Escopo | Descrição |
|---------|--------|-----------|
| `db` | function | Sessão SQLite in-memory (cria e dropa tabelas a cada teste) |
| `client` | function | TestClient do FastAPI com banco de teste injetado |

O `client` usa `dependency_overrides` para substituir o banco real pelo SQLite.

### Exemplo de Teste para Novo Módulo

Ao criar um novo módulo (ex: `roles`), siga este padrão:

**1. Adicionar Factory em `tests/helpers.py`:**

```python
class RoleFactory:
    URL = f"{BASE_URL}/roles"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {"name": f"Role {n}"}
        defaults.update(overrides)
        return defaults

    @classmethod
    def create(cls, client: TestClient, **overrides) -> dict:
        data = cls.build(**overrides)
        response = client.post(cls.URL, json=data)
        assert response.status_code == 201
        return response.json()

    @classmethod
    def create_many(cls, client: TestClient, count: int) -> list[dict]:
        return [cls.create(client) for _ in range(count)]

    @classmethod
    def reset(cls):
        cls._counter = 0
```

**2. Registrar reset no `conftest.py`:**

```python
from tests.helpers import UserFactory, RoleFactory

# dentro da fixture client:
UserFactory.reset()
RoleFactory.reset()
```

**3. Criar `tests/test_roles.py`:**

```python
from tests.helpers import RoleFactory, assert_not_found, assert_validation_error


class TestCreateRole:
    def test_success(self, client):
        role = RoleFactory.create(client, name="admin")
        assert role["name"] == "admin"

    def test_missing_name(self, client):
        response = client.post(RoleFactory.URL, json={})
        assert_validation_error(response, fields=["body.name"])


class TestGetRole:
    def test_not_found(self, client):
        response = client.get(f"{RoleFactory.URL}/999")
        assert_not_found(response)
```

### Cobertura

O projeto mantém **100% de cobertura** em todos os arquivos:

```
Name                                   Stmts   Miss  Cover
--------------------------------------------------------------------
src/common/repository.py                  41      0   100%
src/common/router.py                      32      0   100%
src/core/errors/errors.py                 58      0   100%
src/core/errors/handlers.py               59      0   100%
...
--------------------------------------------------------------------
TOTAL                                    349      0   100%
```
