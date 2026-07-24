# Добавление модуля

Это руководство описывает текущее состояние `mcp-russia`: новые модули нужно добавлять напрямую в `src/mcp_russia/`, потому что автообнаружение уже смотрит в актуальное пространство имён проекта.

## Где создавать новый модуль

Для модуля данных используйте:

```text
src/mcp_russia/data/{modul}/
```

Для агентного модуля используйте:

```text
src/mcp_russia/agenty/{modul}/
```

Минимальная структура пакета:

```text
src/mcp_russia/data/{modul}/
├── __init__.py
├── server.py
├── tools.py
├── client.py
├── schemas.py
└── constants.py
```

## Как это стыкуется с `mcp-russia`

Сейчас корневой сервер:

- публикуется как `mcp_russia.server`;
- автоматически обнаруживает модули в `mcp_russia.data` и `mcp_russia.agenty`;
- монтирует их в единый публичный сервер `mcp-russia`.

Поэтому новый модуль сразу создается в целевом дереве и не требует дополнительного переноса.

## Шаг 1. Описать константы

В `constants.py` храните URL, коды, словари типа перечислений и прочие фиксированные значения.

```python
PRIMER_BAZA_API = "https://api.example.gov/v1"

TIPY_ZAPROSA = {
    "1": "Базовый",
    "2": "Расширенный",
}
```

Правило: не тяните сюда зависимости из других модулей проекта.

## Шаг 2. Описать Pydantic-схемы

В `schemas.py` держите только модели данных:

```python
from pydantic import BaseModel, Field


class PrimerZapisi(BaseModel):
    identifikator: int
    nazvanie: str
    summa: float = Field(description="Сумма в валюте источника")
```

Без сетевых вызовов, без форматирования, без бизнес-логики.

## Шаг 3. Реализовать HTTP-клиент

В `client.py`:

- используйте общие HTTP-утилиты;
- возвращайте типизированные модели;
- не форматируйте ответ под LLM.

```python
from mcp_russia._shared.http_client import http_poluchit

from .constants import PRIMER_BAZA_API
from .schemas import PrimerZapisi


async def spisok_zapisey(stranitsa: int = 1) -> list[PrimerZapisi]:
    dannye = await http_poluchit(f"{PRIMER_BAZA_API}/zapisi", parametry={"stranitsa": stranitsa})
    return [PrimerZapisi(**zapis) for zapis in dannye]
```

## Шаг 4. Описать инструменты

`tools.py` отвечает за пользовательский слой:

- вызывает `client.py`;
- собирает итоговый текст или таблицу;
- содержит понятные строки документации для LLM и разработчиков.

```python
from . import client


async def spisok_zapisey(stranitsa: int = 1) -> str:
    """Возвращает список записей из внешнего источника."""
    zapisi = await client.spisok_zapisey(stranitsa=stranitsa)
    if not zapisi:
        return "Ничего не найдено."
    return "\n".join(f"- {z.nazvanie}" for z in zapisi)
```

## Шаг 5. Зарегистрировать сервер модуля

`server.py` должен экспортировать `mcp: FastMCP`:

```python
from fastmcp import FastMCP

from . import tools


mcp = FastMCP("primer")
mcp.tool(tools.spisok_zapisey)
```

Если у модуля есть ресурсы и промпты, регистрируйте их тут же.

## Шаг 6. Экспортировать `META_FUNKTSII`

В `__init__.py`:

```python
from mcp_russia._shared.feature import MetaFunktsii


META_FUNKTSII = MetaFunktsii(
    imya="primer",
    opisanie="Описание новой интеграции",
    versiya="0.1.0",
    baza_api="https://api.example.gov/v1",
    trebuet_autentifikatsii=False,
    tegi=["primer", "publichnye-dannye"],
)
```

Без `META_FUNKTSII` автообнаружение не увидит пакет.

## Шаг 7. Добавить тесты

Ожидаемая структура:

```text
tests/data/{modul}/
├── test_tools.py
├── test_client.py
└── test_integration.py
```

Проверяйте три слоя:

- форматирование и оркестрацию в `test_tools.py`;
- HTTP-адаптер в `test_client.py`;
- MCP-регистрацию и вызов через `fastmcp.Client` в `test_integration.py`.

## Шаг 8. Проверить регистрацию

Минимум для локальной валидации:

```bash
make test-feature F=primer
make inspect
```

Если изменение крупнее локального модуля, гоняйте `make ci`.

## Соглашения проекта

- Публичное название проекта: `mcp-russia`.
- Публичный импорт: `mcp_russia`.
- Место добавления модулей: `src/mcp_russia/...`.
- Если вы переводите модуль на российские реалии, обновляйте не только код, но и пользовательские тексты, ресурсы, промпты и тестовые ожидания.
