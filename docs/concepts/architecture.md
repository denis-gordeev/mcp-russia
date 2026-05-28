# Архитектура

## Общая схема

На публичном уровне проект позиционируется как `mcp-russia`, но внутренняя feature-структура пока остается в `src/mcp_brasil/`.

```text
src/
├── mcp_russia/
│   ├── __init__.py         # публичный namespace
│   └── server.py           # стабильная точка входа для запуска
└── mcp_brasil/
    ├── server.py           # root server с auto-registry
    ├── settings.py         # конфигурация через env vars
    ├── exceptions.py       # общие исключения
    ├── _shared/            # общая инфраструктура
    ├── data/               # data features
    └── agentes/            # agent features
```

## Что считается публичным API

- пакет для установки: `mcp-russia`;
- импорт для запуска: `mcp_russia.server`;
- команды из `Makefile`, использующие `mcp_russia`.

## Что пока считается internal-слоем

- discovery feature-пакетов в `mcp_brasil.data` и `mcp_brasil.agentes`;
- значительная часть schemas, tools, resources и prompts;
- ряд env-переменных и исторических идентификаторов.

## Root server

Публичная точка входа `mcp_russia.server` просто экспортирует совместимый сервер из internal-дерева. Это позволяет менять внутреннюю структуру постепенно, не ломая внешний импорт.

Фактическая сборка root server сейчас устроена так:

```python
mcp = FastMCP("mcp-russia", lifespan=http_lifespan)
registry = FeatureRegistry()
registry.discover("mcp_brasil.data")
registry.discover("mcp_brasil.agentes")
registry.mount_all(mcp)
```

Следствие простое:

- внешние клиенты работают через `mcp_russia`;
- новые feature пока по-прежнему подключаются в дереве `mcp_brasil`;
- полная физическая миграция может происходить по частям.

## Анатомия feature

Каждая feature остается изолированным пакетом с предсказуемой структурой:

```text
src/mcp_brasil/data/{feature}/
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

Ключевые модули в `mcp_brasil/_shared/`:

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
2. Разработчики могут мигрировать содержимое `mcp_brasil` по частям.
3. Совместимость сохраняется до тех пор, пока не будет готов полный перенос feature-дерева и идентификаторов.
