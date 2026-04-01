# Contributing to mcp-russia

Спасибо за интерес к проекту.

## Быстрый старт

```bash
git clone git@github.com:denis-gordeev/mcp-russia.git
cd mcp-russia
make dev        # Установить зависимости для разработки
make ci         # Запустить lint + mypy + тесты
```

## Структура проекта

```
src/mcp_brasil/
├── server.py           # Корневой сервер (auto-registry, вручную обычно не правится)
├── _shared/            # Общий код (http_client, formatting, cache, rate_limiter)
├── data/               # Features для внешних API
│   ├── ibge/           # Историческая feature исходного проекта
│   ├── transparencia/  # Историческая feature исходного проекта
│   └── {nova_feature}/ # Новая feature данных
└── agentes/            # Features для агентных сценариев
    └── redator/        # Исторический агент официальных документов
```

Публичный namespace для запуска и импорта теперь `mcp_russia`, но внутреннее дерево `src/mcp_brasil/` пока сохранено ради совместимости.

## Как добавить новую feature

1. Создайте каталог `src/mcp_brasil/data/{feature}/` (API) или `src/mcp_brasil/agentes/{feature}/` (агенты) с обязательными файлами:

```
src/mcp_brasil/data/{feature}/      # или agentes/{feature}/
├── __init__.py     # FEATURE_META (обязательно для auto-discovery)
├── server.py       # mcp: FastMCP (обязательно)
├── tools.py        # Функции MCP tools
├── client.py       # Асинхронный HTTP-клиент
├── schemas.py      # Pydantic-модели
└── constants.py    # URL, enum, коды
```

2. В `__init__.py` определите `FEATURE_META`:

```python
from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="minha-feature",
    description="Короткое описание API",
    version="0.1.0",
    api_base="https://api.exemplo.gov.br",
    requires_auth=False,
)
```

3. В `server.py` создайте и зарегистрируйте tools:

```python
from fastmcp import FastMCP
from .tools import minha_tool

mcp = FastMCP("mcp-russia-minha-feature")

mcp.tool(minha_tool)
```

4. Добавьте тесты в `tests/data/{feature}/` (или `tests/agentes/{feature}/`):

```
tests/data/{feature}/         # или tests/agentes/{feature}/
├── test_tools.py             # Mock client, testa lógica
├── test_client.py            # respx mock HTTP
└── test_integration.py       # fastmcp.Client e2e
```

5. Запустите `make ci` и убедитесь, что проверки проходят.

## Поток зависимостей

Внутри каждой feature поток зависимостей однонаправленный:

```
server.py → tools.py → client.py → schemas.py
  регистрирует  оркестрирует  делает HTTP  чистые данные
```

- **`tools.py` не делает HTTP** — делегирует в `client.py`
- **`client.py` не форматирует ответ для LLM** — возвращает Pydantic-модели
- **`schemas.py` без бизнес-логики** — только BaseModel и Field
- **`server.py` только регистрирует** — без бизнес-логики
- **`constants.py` без импортов** из других модулей проекта

## Правила кодовой базы

| Область | Правило | Пример |
|--------|-----------|---------|
| Модули | snake_case | `client.py` |
| Classes | PascalCase | `class Estado(BaseModel)` |
| Функции/tools | snake_case, глагол | `buscar_localidades()` |
| Константы | UPPER_SNAKE | `IBGE_API_BASE` |
| Приватные элементы | `_prefixo` | `_shared/`, `_cache` |

### Инварианты

1. Корневой `server.py` не правится без крайней необходимости — auto-registry делает остальное
2. `tools.py` не делает HTTP-запросы — делегирует в `client.py`
3. `client.py` не форматирует ответы для LLM — возвращает Pydantic models
4. `schemas.py` без бизнес-логики — только модели
5. `server.py` feature только регистрирует — без предметной логики
6. `constants.py` не импортирует другие модули проекта
7. У каждой tool есть docstring — LLM использует ее при выборе вызова
8. Везде async — `async def` в tools и clients
9. Полные type hints во всех функциях

## Технологии

- **Python 3.10+** — базовый язык
- **FastMCP v3** — MCP-фреймворк (`@mcp.tool`, `@mcp.resource`, `@mcp.prompt`)
- **httpx** — HTTP async
- **Pydantic v2** — схемы и валидация
- **uv** — менеджер пакетов
- **ruff** — lint + format (line-length 99)
- **mypy** — type checking (strict)
- **pytest + pytest-asyncio + respx** — тесты

## Тесты

```bash
make test                 # Все тесты
make test-feature F=ibge  # Тесты одной feature
make lint                 # ruff check + format check
make types                # mypy strict
make ci                   # lint + types + test
```

Тесты используют:
- **pytest** + **pytest-asyncio** для async-кода
- **respx** для HTTP-моков в `test_client.py`
- **unittest.mock** для моков клиента в `test_tools.py`
- **fastmcp.Client** для e2e-интеграционных тестов

### Шаблоны тестов

#### `test_tools.py` — мок клиента

```python
from unittest.mock import AsyncMock, patch
import pytest
from mcp_brasil.data.{feature}.tools import buscar_{feature}

@pytest.mark.asyncio
async def test_buscar_retorna_formatado():
    with patch("mcp_brasil.data.{feature}.tools.buscar_exemplo", new_callable=AsyncMock) as mock:
        mock.return_value = [...]
        resultado = await buscar_{feature}("query")
        assert "ожидаемое" in resultado
```

#### `test_client.py` — HTTP-мок через `respx`

```python
import httpx
import pytest
import respx
from mcp_brasil.data.{feature}.client import buscar_exemplo

@pytest.mark.asyncio
@respx.mock
async def test_buscar_sucesso():
    respx.get("https://api.exemplo.gov.br/endpoint").mock(
        return_value=httpx.Response(200, json=[{"id": 1, "nome": "Teste"}])
    )
    resultado = await buscar_exemplo("query")
    assert len(resultado) == 1
```

#### `test_integration.py` — end-to-end через `fastmcp.Client`

```python
import pytest
from fastmcp import Client
from mcp_brasil.data.{feature}.server import mcp

@pytest.mark.asyncio
async def test_tool_via_mcp_client():
    async with Client(mcp) as client:
        result = await client.call_tool("buscar_{feature}", {"query": "teste"})
        assert result is not None
```

## Коммиты

Используйте **Conventional Commits** (на русском или английском):

```
feat(ibge): add tool consultar_populacao
fix(bacen): handle empty response from SGS
test(transparencia): add edge-case tests for client
docs: update README with new feature
refactor(camara): simplify pagination logic
```

- Перед коммитом убедитесь, что `make ci` проходит
- Не копите несвязанные изменения в одном коммите

## Релизы

Релизы следуют **Semantic Versioning**.

### Типы повышения версии

| Ситуация | Bump | Пример |
|----------|------|---------|
| Новая feature (новое API, новый агент) | **minor** | `feat(saude): add 5 tools` |
| Исправление бага, корректировка endpoint | **patch** | `fix(bacen): handle timeout` |
| Breaking change (переименование tools, изменение API) | **major** | refactor, ломающий клиентов |
| Только docs, тесты, внутренний refactor | **нет** | Релиз не обязателен |

### Как сделать релиз

```bash
make version          # Показать текущую версию
make release-patch    # Повысить patch (сначала запускает CI)
make release-minor    # Bump minor
make release-major    # Bump major
make changelog        # Сгенерировать CHANGELOG.md вручную
make build            # Build do pacote (sdist + wheel)
```

### CI/CD

- **CI** (`.github/workflows/ci.yml`): запускается на каждый push/PR в `main` — lint + types + тесты (Python 3.10-3.13)
- **Release** (`.github/workflows/release.yml`): запускается по тегу `v*` — CI + build + publish в PyPI + GitHub Release

### Инфраструктура

- Версия задается в `pyproject.toml`
- `__init__.py` использует `importlib.metadata` для чтения версии без дублирования
- `CHANGELOG.md` генерируется через `git-cliff` (`cliff.toml`)
- `semantic-release` настроен в `pyproject.toml` (`[tool.semantic_release]`)

## Pull request

- Используйте **Conventional Commits** в заголовке PR
- Перед открытием PR убедитесь, что `make ci` проходит
- Опишите, что изменилось и зачем
- Для новой feature добавляйте тесты (`test_tools.py`, `test_client.py`, `test_integration.py`)
- Если обнаружили технический долг или следующий шаг миграции, зафиксируйте его в `TODO.md`
