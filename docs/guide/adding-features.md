# Добавление feature

Этот гид описывает текущее состояние `mcp-russia`: новые feature нужно добавлять напрямую в `src/mcp_russia/`, потому что auto-discovery уже смотрит в актуальный namespace проекта.

## Где создавать новую feature

Для data-feature используйте:

```text
src/mcp_russia/data/{feature}/
```

Для agent-feature используйте:

```text
src/mcp_russia/agenty/{feature}/
```

Минимальная структура пакета:

```text
src/mcp_russia/data/{feature}/
├── __init__.py
├── server.py
├── tools.py
├── client.py
├── schemas.py
└── constants.py
```

## Как это стыкуется с `mcp-russia`

Сейчас root server:

- публикуется как `mcp_russia.server`;
- автоматически обнаруживает features в `mcp_russia.data` и `mcp_russia.agenty`;
- монтирует их в единый публичный сервер `mcp-russia`.

Поэтому новая feature сразу создается в целевом дереве и не требует дополнительного переноса.

## Шаг 1. Описать constants

В `constants.py` храните URL, коды, enum-подобные словари и прочие фиксированные значения.

```python
PRIMER_API_BASE = "https://api.example.gov/v1"

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
    id: int
    name: str
    amount: float = Field(description="Сумма в валюте источника")
```

Без сетевых вызовов, без форматирования, без бизнес-логики.

## Шаг 3. Реализовать HTTP-клиент

В `client.py`:

- используйте shared HTTP helpers;
- возвращайте типизированные модели;
- не форматируйте ответ под LLM.

```python
from mcp_russia._shared.http_client import http_get

from .constants import PRIMER_API_BASE
from .schemas import PrimerZapisi


async def spisok_zapisey(page: int = 1) -> list[PrimerZapisi]:
    data = await http_get(f"{PRIMER_API_BASE}/items", params={"page": page})
    return [PrimerZapisi(**item) for item in data]
```

## Шаг 4. Описать tools

`tools.py` отвечает за пользовательский слой:

- вызывает `client.py`;
- собирает итоговый текст или таблицу;
- содержит понятные docstring для LLM и разработчиков.

```python
from . import client


async def spisok_zapisey(page: int = 1) -> str:
    """Возвращает список записей из внешнего источника."""
    zapisi = await client.spisok_zapisey(page=page)
    if not zapisi:
        return "Ничего не найдено."
    return "\n".join(f"- {z.name}" for z in zapisi)
```

## Шаг 5. Зарегистрировать feature-server

`server.py` должен экспортировать `mcp: FastMCP`:

```python
from fastmcp import FastMCP

from . import tools


mcp = FastMCP("example")
mcp.tool(tools.spisok_zapisey)
```

Если у feature есть resources и prompts, регистрируйте их тут же.

## Шаг 6. Экспортировать `FEATURE_META`

В `__init__.py`:

```python
from mcp_russia._shared.feature import FeatureMeta


FEATURE_META = FeatureMeta(
    name="example",
    description="Описание новой интеграции",
    version="0.1.0",
    api_base="https://api.example.gov/v1",
    requires_auth=False,
    tags=["example", "public-data"],
)
```

Без `FEATURE_META` auto-discovery не увидит пакет.

## Шаг 7. Добавить тесты

Ожидаемая структура:

```text
tests/data/{feature}/
├── test_tools.py
├── test_client.py
└── test_integration.py
```

Проверяйте три слоя:

- форматирование и orchestration в `test_tools.py`;
- HTTP-адаптер в `test_client.py`;
- MCP-регистрацию и вызов через `fastmcp.Client` в `test_integration.py`.

## Шаг 8. Проверить регистрацию

Минимум для локальной валидации:

```bash
make test-feature F=example
make inspect
```

Если изменение крупнее локальной feature, гоняйте `make ci`.

## Что важно помнить при миграции

- Новый публичный бренд проекта: `mcp-russia`.
- Новый публичный импорт: `mcp_russia`.
- Текущее место добавления feature: `src/mcp_russia/...`.
- Если вы переводите feature на российские реалии, обновляйте не только код, но и пользовательские тексты, ресурсы, prompts и тестовые ожидания.
