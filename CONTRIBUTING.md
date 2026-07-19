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
├── server.py           # Корневой сервер (автообнаружение, вручную обычно не правится)
├── settings.py         # Конфигурация через переменные окружения
├── exceptions.py       # Общие исключения проекта
├── _shared/            # Общий код (http-клиент, форматирование, кеш, ограничитель частоты)
├── data/               # Модули для внешних API
│   ├── cbrf/           # Центральный банк РФ
│   ├── rosstat/        # Росстат
│   └── {novyy_modul}/ # Новый модуль данных
└── agenty/             # Модули для агентных сценариев
    └── deloproizvodstvo/        # Агент официальных документов
```

Рабочее пространство имён для запуска и импорта: `mcp_russia`.

## Как добавить новый модуль

1. Создайте каталог `src/mcp_russia/data/{modul}/` (API) или `src/mcp_russia/agenty/{modul}/` (агенты) с обязательными файлами:

```
src/mcp_russia/data/{modul}/      # или agenty/{modul}/
├── __init__.py     # META_FUNKTSII (обязательно для автообнаружения)
├── server.py       # mcp: FastMCP (обязательно)
├── tools.py        # Функции MCP-инструментов
├── client.py       # Асинхронный HTTP-клиент
├── schemas.py      # Pydantic-модели
└── constants.py    # URL, перечисления, коды
```

2. В `__init__.py` определите `META_FUNKTSII`:

```python
from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="primer-modul",
    opisanie="Короткое описание API",
    versiya="0.1.0",
    baza_api="https://api.example.gov.ru",
    trebuet_autentifikatsii=False,
)
```

3. В `server.py` создайте и зарегистрируйте инструменты:

```python
from fastmcp import FastMCP
from .tools import primer_instrument

mcp = FastMCP("mcp-russia-primer-modul")

mcp.tool(primer_instrument)
```

4. Добавьте тесты в `tests/data/{modul}/` (или `tests/agenty/{modul}/`):

```
tests/data/{modul}/         # или tests/agenty/{modul}/
├── test_tools.py             # Мок клиента, проверяет логику
├── test_client.py            # respx мок HTTP
└── test_integration.py       # fastmcp.Client сквозное тестирование
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
| Классы | PascalCase | `class Subjekt(BaseModel)` |
| Функции/инструменты | snake_case, глагол | `poisk_mestopolozheniy()` |
| Константы | UPPER_SNAKE | `ROSSTAT_BAZA_API` |
| Приватные элементы | `_prefiks` | `_shared/`, `_cache` |

### Инварианты

1. Корневой `server.py` не правится без крайней необходимости — автообнаружение делает остальное
2. `tools.py` не делает HTTP-запросы — делегирует в `client.py`
3. `client.py` не форматирует ответы для LLM — возвращает модели Pydantic
4. `schemas.py` без бизнес-логики — только модели
5. `server.py` модуля только регистрирует — без предметной логики
6. `constants.py` не импортирует другие модули проекта
7. У каждого инструмента есть строка документации — LLM использует её при выборе вызова
8. Везде async — `async def` в tools и clients
9. Полные type hints во всех функциях

## Технологии

- **Python 3.10+** — базовый язык
- **FastMCP v3** — MCP-фреймворк (`@mcp.tool`, `@mcp.resource`, `@mcp.prompt`)
- **httpx** — HTTP async
- **Pydantic v2** — схемы и валидация
- **uv** — менеджер пакетов
- **ruff** — линтер + форматирование (длина строки 99)
- **mypy** — проверка типов (строгий режим)
- **pytest + pytest-asyncio + respx** — тесты

## Тесты

```bash
make test                 # Все тесты
make test-feature F=cbrf  # Тесты одного модуля
make lint                 # проверка линтером + проверка форматирования
make types                # mypy в строгом режиме
make ci                   # линтер + типы + тесты
```

Тесты используют:
- **pytest** + **pytest-asyncio** для async-кода
- **respx** для HTTP-моков в `test_client.py`
- **unittest.mock** для моков клиента в `test_tools.py`
- **fastmcp.Client** для сквозных интеграционных тестов

### Шаблоны тестов

#### `test_tools.py` — мок клиента

```python
from unittest.mock import AsyncMock, patch
import pytest
from mcp_russia.data.{modul}.tools import poisk_{modul}

@pytest.mark.asyncio
async def test_poisk_vozvrashaet_otformatirovannoe():
        with patch("mcp_russia.data.{modul}.tools.poisk_primera", new_callable=AsyncMock) as maket:
        maket.return_value = [...]
        rezultat = await poisk_{modul}("zapros")
        assert "ozhidaemoe" in rezultat
```

#### `test_client.py` — HTTP-мок через `respx`

```python
import httpx
import pytest
import respx
from mcp_russia.data.{modul}.client import poisk_primera

@pytest.mark.asyncio
@respx.mock
async def test_poisk_uspeshen():
    respx.get("https://api.example.gov.ru/konechnaya_tochka").mock(
        return_value=httpx.Response(200, json=[{"identifikator": 1, "nazvanie": "Проверка"}])
    )
    rezultat = await poisk_primera("zapros")
    assert len(rezultat) == 1
```

#### `test_integration.py` — сквозное тестирование через `fastmcp.Client`

```python
import pytest
from fastmcp import Client
from mcp_russia.data.{modul}.server import mcp

@pytest.mark.asyncio
async def test_tool_via_mcp_client():
    async with Client(mcp) as klient:
        rezultat = await klient.call_tool("poisk_{modul}", {"zapros": "proverka"})
        assert rezultat is not None
```

## Коммиты

Используйте **Конвенциональные коммиты** (на русском или английском):

```
feat(cbrf): добавить инструмент poluchit_dinamiku_kursa
fix(fns): обработать пустой ответ ЕГРЮЛ
test(zakupki): добавить граничные тесты для клиента
docs: обновить README с новым модулем
refactor(gosduma): упростить логику пагинации
```

- Перед коммитом убедитесь, что `make ci` проходит
- Не копите несвязанные изменения в одном коммите
- Не удаляйте работающие модули без явной подготовки замены

## Релизы

Релизы следуют **семантическому версионированию**.

### Типы повышения версии

| Ситуация | Повышение | Пример |
|----------|------|---------|
| Новый модуль (новое API, новый агент) | **minor** | `feat(minzdrav): добавить 5 инструментов` |
| Исправление бага, корректировка конечной точки | **patch** | `fix(cbrf): обработать таймаут` |
| Критическое изменение (переименование инструментов, изменение API) | **major** | рефакторинг, ломающий клиентов |
| Только docs, тесты, внутренний рефакторинг | **нет** | Релиз не обязателен |

### Как сделать релиз

```bash
make version          # Показать текущую версию
make release-patch    # Повысить patch (сначала запускает CI)
make release-minor    # Повысить minor
make release-major    # Повысить major
make changelog        # Сгенерировать CHANGELOG.md вручную
make build            # Сборка пакета (исходный дистрибутив + wheel-пакет)
```

### CI/CD

- **CI** (`.github/workflows/ci.yml`): запускается при каждом отправлении изменений/пул-реквесте в `main` — линтер + типы + тесты (Python 3.10-3.13)
- **Release** (`.github/workflows/release.yml`): запускается по тегу `v*` — CI + сборка + публикация в PyPI + релиз на GitHub

### Инфраструктура

- Версия задается в `pyproject.toml`
- `__init__.py` использует `importlib.metadata` для чтения версии без дублирования
- `CHANGELOG.md` генерируется через `git-cliff` (`cliff.toml`)
- `semantic-release` настроен в `pyproject.toml` (`[tool.semantic_release]`)

## Pull-запрос

- Используйте **Конвенциональные коммиты** в заголовке пул-реквеста
- Перед открытием пул-реквеста убедитесь, что `make ci` проходит
- Опишите, что изменилось и зачем
- Для нового модуля добавляйте тесты (`test_tools.py`, `test_client.py`, `test_integration.py`)
- Если обнаружили технический долг или следующий шаг миграции, зафиксируйте его в `TODO.md`
