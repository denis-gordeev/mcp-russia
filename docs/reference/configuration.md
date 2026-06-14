# Конфигурация

Эта страница описывает публичную конфигурацию `mcp-russia`.

## Переменные окружения

### API-ключи

| Переменная | По умолчанию | Описание |
|----------|--------------|----------|
| `ANTHROPIC_API_KEY` | — | Нужен для meta-tools `rekomendovat_instrumenty` и `splanirovat_zapros` |

### Настройки сервера

| Переменная | По умолчанию | Описание |
|----------|--------------|----------|
| `MCP_RUSSIA_TOOL_SEARCH` | `bm25` | Режим discovery и публикации tools для LLM |
| `MCP_RUSSIA_HTTP_TIMEOUT` | `30.0` | HTTP timeout в секундах |
| `MCP_RUSSIA_HTTP_MAX_RETRIES` | `3` | Максимальное число повторных попыток |
| `MCP_RUSSIA_HTTP_BACKOFF_BASE` | `1.0` | Базовая задержка для экспоненциального backoff |
| `MCP_RUSSIA_USER_AGENT` | `mcp-russia/<version>` | Значение `User-Agent` для исходящих HTTP-запросов |

## `MCP_RUSSIA_TOOL_SEARCH`

Переменная управляет тем, как набор инструментов показывается модели:

| Значение | Поведение | Когда использовать |
|----------|-----------|--------------------|
| `bm25` | Показывает только top-N релевантных инструментов, мета-инструменты остаются доступными всегда | Базовый режим |
| `none` | Публикует весь каталог инструментов без фильтрации | Отладка, ручная проверка, очень большой контекст |
| `code_mode` | Экспериментальный режим discovery через `get_tags`, `search` и `GetSchemas` | Продвинутые сценарии и внутренние тесты |

### Anthropic API

Нужен только для meta-tools `rekomendovat_instrumenty` и `splanirovat_zapros`. Остальные features продолжают работать без него.

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
        "ANTHROPIC_API_KEY": "your-key",
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
  -e ANTHROPIC_API_KEY=your-key \
  -- uvx --from mcp-russia python -m mcp_russia.server
```

### HTTP transport

```bash
ANTHROPIC_API_KEY=xxx \
  fastmcp run mcp_russia.server:mcp --transport http --port 8000
```

## HTTP-клиент

Общий `httpx` client поддерживает retry, backoff и единые timeout-настройки.

### Retry с backoff

Повтор выполняется автоматически при:

- `429` и с учетом `Retry-After`
- `5xx`, если источник временно недоступен
- timeout, если API отвечает дольше `MCP_RUSSIA_HTTP_TIMEOUT`
- сетевых ошибках соединения или DNS

Базовая схема backoff: `1s -> 2s -> 4s`, с опорой на `MCP_RUSSIA_HTTP_BACKOFF_BASE` и ограничением `MCP_RUSSIA_HTTP_MAX_RETRIES`.

### Rate limiting

Отдельные features могут использовать общий `RateLimiter` из `src/mcp_russia/_shared/rate_limiter.py`:

```python
limiter = RateLimiter(max_requests=5, period=1.0)

async with limiter:
    data = await http_get(url)
```
