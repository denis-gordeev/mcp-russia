# Участие в разработке mcp-russia

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
src/mcp_russia/
├── server.py           # Корневой сервер (auto-registry, вручную обычно не правится)
├── settings.py         # Конфигурация через env vars
├── exceptions.py       # Общие исключения проекта
├── _shared/            # Общий код (http_client, formatting, cache, rate_limiter)
├── data/               # Модули для внешних API
│   ├── cbrf/           # Центральный банк РФ
│   ├── rosstat/        # Росстат
│   └── {novaya_feature}/ # Новый модуль данных
└── agenty/             # Модули для агентных сценариев
    └── redator/        # Агент официальных документов
```

Рабочий namespace для запуска и импорта: `mcp_russia`.

## Как добавить новый модуль

1. Создайте каталог `src/mcp_russia/data/{feature}/` (API) или `src/mcp_russia/agenty/{feature}/` (агенты) с обязательными файлами:

```
src/mcp_russia/data/{feature}/      # или agenty/{feature}/
├── __init__.py     # META_FUNKTSII (обязательно для автообнаружения)
├── server.py       # mcp: FastMCP (обязательно)
├── tools.py        # Функции MCP-инструментов
├── client.py       # Асинхронный HTTP-клиент
├── schemas.py      # Pydantic-модели
└── constants.py    # URL, enum, коды
```

2. В `__init__.py` определите `META_FUNKTSII`:

```python
from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="primer-feature",
    opisanie="Короткое описание API",
    versiya="0.1.0",
    baza_api="https://api.example.gov.ru",
    trebuet_autentifikatsii=False,
)
```

3. В `server.py` создайте и зарегистрируйте tools:

```python
from fastmcp import FastMCP
from .tools import primer_tool

mcp = FastMCP("mcp-russia-primer-feature")

mcp.tool(primer_tool)
```

4. Добавьте тесты в `tests/data/{feature}/` (или `tests/agenty/{feature}/`):

```
tests/data/{feature}/         # или tests/agenty/{feature}/
├── test_tools.py             # Mock client, проверяет логику
├── test_client.py            # respx mock HTTP
└── test_integration.py       # fastmcp.Client e2e
```

5. Запустите `make ci` и убедитесь, что проверки проходят.

## Поток зависимостей

Внутри каждого модуля поток зависимостей однонаправленный:

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
| Classes | PascalCase | `class Subjekt(BaseModel)` |
| Функции/tools | snake_case, глагол | `poisk_mestopolozheniy()` |
| Константы | UPPER_SNAKE | `ROSSTAT_API_BASE` |
| Приватные элементы | `_prefiks` | `_shared/`, `_cache` |

### Инварианты

1. Корневой `server.py` не правится без крайней необходимости — auto-registry делает остальное
2. `tools.py` не делает HTTP-запросы — делегирует в `client.py`
3. `client.py` не форматирует ответы для LLM — возвращает модели Pydantic
4. `schemas.py` без бизнес-логики — только модели
5. `server.py` модуля только регистрирует — без предметной логики
6. `constants.py` не импортирует другие модули проекта
7. У каждого инструмента есть docstring — LLM использует её при выборе вызова
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
make test-feature F=cbrf  # Тесты одного модуля
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
from mcp_russia.data.{feature}.tools import poisk_{feature}

@pytest.mark.asyncio
async def test_poisk_vozvrashaet_otformatirovannoe():
    with patch("mcp_russia.data.{feature}.tools.poisk_primera", new_callable=AsyncMock) as mock:
        mock.return_value = [...]
        rezultat = await poisk_{feature}("zapros")
        assert "ozhidaemoe" in rezultat
```

#### `test_client.py` — HTTP-мок через `respx`

```python
import httpx
import pytest
import respx
from mcp_russia.data.{feature}.client import poisk_primera

@pytest.mark.asyncio
@respx.mock
async def test_poisk_uspeshen():
    respx.get("https://api.example.gov.ru/endpoint").mock(
        return_value=httpx.Response(200, json=[{"id": 1, "nazvanie": "Test"}])
    )
    rezultat = await poisk_primera("zapros")
    assert len(rezultat) == 1
```

#### `test_integration.py` — end-to-end через `fastmcp.Client`

```python
import pytest
from fastmcp import Client
from mcp_russia.data.{feature}.server import mcp

@pytest.mark.asyncio
async def test_tool_via_mcp_client():
    async with Client(mcp) as client:
        result = await client.call_tool("poisk_{feature}", {"zapros": "test"})
        assert result is not None
```

## Коммиты

Используйте **Conventional Commits** (на русском или английском):

```
feat(cbrf): add tool poluchit_dinamiku_kursa
fix(fns): handle empty response from EGRUL
test(zakupki): add edge-case tests for client
docs: обновить README с новым модулем
refactor(gosduma): simplify pagination logic
```

- Перед коммитом убедитесь, что `make ci` проходит
- Не копите несвязанные изменения в одном коммите
- Не удаляйте работающие модули без явной подготовки замены

## Релизы

Релизы следуют **Semantic Versioning**.

### Типы повышения версии

| Ситуация | Bump | Пример |
|----------|------|---------|
| Новый модуль (новое API, новый агент) | **minor** | `feat(minzdrav): add 5 tools` |
| Исправление бага, корректировка endpoint | **patch** | `fix(cbrf): handle timeout` |
| Критическое изменение (переименование инструментов, изменение API) | **major** | refactor, ломающий клиентов |
| Только docs, тесты, внутренний refactor | **нет** | Релиз не обязателен |

### Как сделать релиз

```bash
make version          # Показать текущую версию
make release-patch    # Повысить patch (сначала запускает CI)
make release-minor    # Bump minor
make release-major    # Bump major
make changelog        # Сгенерировать CHANGELOG.md вручную
make build            # Сборка пакета (sdist + wheel)
```

### CI/CD

- **CI** (`.github/workflows/ci.yml`): запускается на каждый push/PR в `main` — lint + types + тесты (Python 3.10-3.13)
- **Release** (`.github/workflows/release.yml`): запускается по тегу `v*` — CI + build + publish в PyPI + GitHub Release

### Инфраструктура

- Версия задается в `pyproject.toml`
- `__init__.py` использует `importlib.metadata` для чтения версии без дублирования
- `CHANGELOG.md` генерируется через `git-cliff` (`cliff.toml`)
- `semantic-release` настроен в `pyproject.toml` (`[tool.semantic_release]`)

## Pull-запрос

- Используйте **Conventional Commits** в заголовке PR
- Перед открытием PR убедитесь, что `make ci` проходит
- Опишите, что изменилось и зачем
- Для нового модуля добавляйте тесты (`test_tools.py`, `test_client.py`, `test_integration.py`)
- Если обнаружили технический долг или следующий шаг миграции, зафиксируйте его в `TODO.md`
