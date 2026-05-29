# Архитектура

## Общая схема

Текущая рабочая структура проекта уже находится в `src/mcp_russia/`. Исторические упоминания `mcp_brasil` в документации относятся к предыдущему этапу миграции и не описывают актуальный runtime.

```text
src/
└── mcp_russia/
    ├── __init__.py         # публичный namespace
    ├── server.py           # root server с auto-registry
    ├── settings.py         # конфигурация через env vars
    ├── exceptions.py       # общие исключения
    ├── _shared/            # общая инфраструктура
    ├── data/               # data features
    └── agenty/             # agent features
```

## Что считается публичным API

- пакет для установки: `mcp-russia`;
- импорт для запуска: `mcp_russia.server`;
- команды из `Makefile`, использующие `mcp_russia`.

## Что пока считается internal-слоем

- shared-инфраструктура и feature-дерево внутри `mcp_russia`;
- значительная часть schemas, tools, resources и prompts, унаследованных от исходного проекта;
- ряд narrative-артефактов и справочных текстов, где еще встречаются старые имена и бразильский контекст.

## Root server

Публичная точка входа `mcp_russia.server` является и фактическим root server, и стабильным импортом для внешних клиентов.

Фактическая сборка root server сейчас устроена так:

```python
mcp = FastMCP("mcp-russia", lifespan=http_lifespan)
registry = FeatureRegistry()
registry.discover("mcp_russia.data")
registry.discover("mcp_russia.agenty")
registry.mount_all(mcp)
```

Следствие простое:

- внешние клиенты работают через `mcp_russia`;
- новые feature должны добавляться сразу в `mcp_russia`;
- дальнейшая миграция сместилась из физического переноса пакета в зачистку документации, legacy narrative и источников данных.

## Анатомия feature

Каждая feature остается изолированным пакетом с предсказуемой структурой:

```text
src/mcp_russia/data/{feature}/
├── __init__.py
├── server.py
├── tools.py
├── client.py
├── schemas.py
└── constants.py
```

Распределение ответственности:

- `server.py` регистрирует tools, resources и prompts;
- `tools.py` оркестрирует пользовательские запросы;
- `client.py` делает HTTP-вызовы и возвращает типизированные данные;
- `schemas.py` хранит Pydantic-модели;
- `constants.py` описывает URL, коды и справочные значения.

## Shared-инфраструктура

Ключевые модули в `mcp_russia/_shared/`:

| Модуль | Назначение |
|--------|------------|
| `feature.py` | discovery и registry feature-пакетов |
| `http_client.py` | общий async HTTP-клиент с retry |
| `cache.py` | TTL-cache и decorator для кеширования |
| `formatting.py` | табличное и числовое форматирование |
| `rate_limiter.py` | rate limiting для внешних API |
| `batch.py` | выполнение нескольких tool-call за один запрос |
| `discovery.py` | каталог и рекомендация tools |
| `planner.py` | построение плана запроса |
| `lifespan.py` | общий lifecycle для HTTP-клиента |

## Meta-tools root server

Поверх feature-инструментов root server регистрирует meta-tools:

- `spisok_funktsiy`;
- `rekomendovat_instrumenty`;
- `splanirovat_zapros`;
- `vypolnit_paket`.

Они дают обзор доступных интеграций, помогают подобрать инструменты и собрать составной запрос без ручного перебора feature-модулей.

## Архитектурная цель миграции

Текущее устройство специально разделяет внешний и внутренний слой:

1. Пользователи уже работают с `mcp-russia`.
2. Разработчики продолжают поэтапно очищать legacy-слой без смены публичной точки входа.
3. Совместимость сохраняется до тех пор, пока не будут убраны оставшиеся исторические идентификаторы и narrative-ссылки.
