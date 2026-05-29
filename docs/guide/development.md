# Разработка

## Локальный setup

```bash
git clone git@github.com:denis-gordeev/mcp-russia.git
cd mcp-russia
make dev
```

Требования:

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Основные команды

| Команда | Назначение |
|---------|------------|
| `make sync` | установить production-зависимости |
| `make dev` | установить production + dev зависимости |
| `make test` | запустить весь test suite |
| `make test-feature F=ibge` | прогнать тесты одной feature |
| `make lint` | `ruff check` + `ruff format --check` |
| `make fix` | auto-fix для lint и форматирования |
| `make types` | `mypy` по `src/mcp_russia/` |
| `make ci` | полный локальный quality gate |
| `make run` | запуск MCP-сервера по stdio |
| `make serve` | запуск MCP-сервера по HTTP |
| `make inspect` | вывести summary зарегистрированных features |
| `make build` | собрать wheel и sdist |

## Переходная особенность кодовой базы

Основной runtime и исходники уже переведены в `src/mcp_russia/`. Переходный слой теперь проявляется в основном в документации, historical narrative и части legacy-названий внутри features.

Практическое правило:

- пользовательские сценарии и документация должны двигаться к `mcp_russia`;
- новые кодовые изменения и новые features должны добавляться в `mcp_russia`.

## Структура тестов

Тесты по-прежнему зеркалят internal-дерево:

```text
tests/
├── conftest.py
├── test_root_server.py
├── test_discovery.py
├── test_public_namespace.py
├── _shared/
├── data/
└── agenty/
```

Типовой расклад внутри feature:

- `test_tools.py` проверяет orchestration и форматирование;
- `test_client.py` проверяет HTTP-слой с моками;
- `test_integration.py` проверяет регистрацию и вызов через `fastmcp.Client`.

## Проверки перед фиксацией изменений

Минимальный набор:

```bash
make lint
make types
make test
```

Если меняется одна feature или один раздел документации, можно сузить проверки, но это должно быть осознанное решение.

## CI и поддерживаемые версии

Проект ориентируется на Python 3.10-3.13. Локально достаточно держать совместимость с настройками из `pyproject.toml` и не ломать команды `make ci`.

## Коммиты

Предпочтительный стиль:

```text
feat(feature): краткое описание
fix(scope): краткое описание
docs: актуализировать русскоязычную документацию
test(scope): добавить покрытие
```

## Contribution workflow

1. Работайте от `main` или отдельной ветки, если изменение заметное.
2. Не удаляйте compatibility-слой без явной подготовки замены.
3. Если меняете поведение feature, обновляйте код, тесты и документацию вместе.
4. Если меняете только публичное позиционирование, проверяйте, что команды запуска и импорты остаются рабочими.
5. Перед PR убедитесь, что `make ci` или релевантный поднабор проверок проходит.
