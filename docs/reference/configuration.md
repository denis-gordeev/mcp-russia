# Конфигурация

Эта страница описывает публичную конфигурацию `mcp-russia`.

## Переменные окружения

### API-ключи

| Переменная | По умолчанию | Описание |
|----------|--------------|----------|
| `ANTHROPIC_API_KEY` | — | Нужен для мета-инструментов `rekomendovat_instrumenty` и `splanirovat_zapros` |

### Настройки сервера

| Переменная | По умолчанию | Описание |
|----------|--------------|----------|
| `MCP_RUSSIA_TOOL_SEARCH` | `bm25` | Режим обнаружения и публикации инструментов для LLM |
| `MCP_RUSSIA_HTTP_TIMEOUT` | `30.0` | HTTP timeout в секундах |
| `MCP_RUSSIA_HTTP_MAX_RETRIES` | `3` | Максимальное число повторных попыток |
| `MCP_RUSSIA_HTTP_BACKOFF_BASE` | `1.0` | Базовая задержка для экспоненциального отката |
| `MCP_RUSSIA_USER_AGENT` | `mcp-russia/<version>` | Значение `User-Agent` для исходящих HTTP-запросов |

## `MCP_RUSSIA_TOOL_SEARCH`

Переменная управляет тем, как набор инструментов показывается модели:

| Значение | Поведение | Когда использовать |
|----------|-----------|--------------------|
| `bm25` | Показывает только top-N релевантных инструментов, мета-инструменты остаются доступными всегда | Базовый режим |
| `none` | Публикует весь каталог инструментов без фильтрации | Отладка, ручная проверка, очень большой контекст |
| `code_mode` | Экспериментальный режим обнаружения через `get_tags`, `search` и `GetSchemas` | Продвинутые сценарии и внутренние тесты |

### Anthropic API

Нужен только для мета-инструментов `rekomendovat_instrumenty` и `splanirovat_zapros`. Остальные модули продолжают работать без него.

Установите `ANTHROPIC_API_KEY=<ваш-ключ>`.

## Настройка клиентов

### Claude Desktop

```json
{
  "mcpServers": {
    "mcp-russia": {
      "command": "uvx",
      "args": ["--from", "mcp-russia", "python", "-m", "mcp_russia.server"],
      "env": {
        "ANTHROPIC_API_KEY": "ваш-ключ",
        "MCP_RUSSIA_TOOL_SEARCH": "bm25"
      }
    }
  }
}
```

### VS Code / Cursor

```json
{
  "servers": {
    "mcp-russia": {
      "command": "uvx",
      "args": ["--from", "mcp-russia", "python", "-m", "mcp_russia.server"],
      "env": {
        "MCP_RUSSIA_TOOL_SEARCH": "bm25"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add mcp-russia -- uvx --from mcp-russia python -m mcp_russia.server
```

Если нужны переменные окружения:

```bash
claude mcp add mcp-russia \
  -e ANTHROPIC_API_KEY=ваш-ключ \
  -- uvx --from mcp-russia python -m mcp_russia.server
```

### HTTP-транспорт

```bash
ANTHROPIC_API_KEY=xxx \
  fastmcp run mcp_russia.server:mcp --transport http --port 8000
```

## HTTP-клиент

Общий `httpx` клиент поддерживает повторные попытки, экспоненциальный откат и единые настройки таймаута.

### Повторные попытки с экспоненциальной задержкой

Повтор выполняется автоматически при:

- `429` и с учетом `Retry-After`
- `5xx`, если источник временно недоступен
- timeout, если API отвечает дольше `MCP_RUSSIA_HTTP_TIMEOUT`
- сетевых ошибках соединения или DNS

Базовая схема отката: `1с -> 2с -> 4с`, с опорой на `MCP_RUSSIA_HTTP_BACKOFF_BASE` и ограничением `MCP_RUSSIA_HTTP_MAX_RETRIES`.

### Ограничение частоты запросов

Отдельные модули могут использовать общий `OgranichitelChastoty` из `src/mcp_russia/_shared/rate_limiter.py`:

```python
ogranichitel = OgranichitelChastoty(maks_zaprosov=5, period=1.0)

async with ogranichitel:
    dannye = await http_poluchit(adres_url)
```
