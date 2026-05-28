# Конфигурация

Эта страница описывает публичную конфигурацию `mcp-russia`. Часть интеграций пока остается legacy-слоем исходного проекта, поэтому рядом с новыми переменными еще поддерживаются исторические алиасы `MCP_BRASIL_*`.

## Переменные окружения

### API-ключи

| Переменная | По умолчанию | Описание |
|----------|--------------|----------|
| `TRANSPARENCIA_API_KEY` | — | Ключ для legacy-интеграции с Portal da Transparencia |
| `DATAJUD_API_KEY` | — | Ключ для legacy-интеграции с DataJud / CNJ |
| `ANTHROPIC_API_KEY` | — | Нужен для meta-tools `rekomendovat_instrumenty` и `splanirovat_zapros` |

### Настройки сервера

| Переменная | По умолчанию | Описание |
|----------|--------------|----------|
| `MCP_RUSSIA_TOOL_SEARCH` | `bm25` | Режим discovery и публикации tools для LLM |
| `MCP_RUSSIA_HTTP_TIMEOUT` | `30.0` | HTTP timeout в секундах |
| `MCP_RUSSIA_HTTP_MAX_RETRIES` | `3` | Максимальное число повторных попыток |
| `MCP_RUSSIA_HTTP_BACKOFF_BASE` | `1.0` | Базовая задержка для экспоненциального backoff |
| `MCP_RUSSIA_USER_AGENT` | `mcp-russia/<version>` | Значение `User-Agent` для исходящих HTTP-запросов |

Исторические алиасы `MCP_BRASIL_*` пока работают как fallback и нужны только для совместимости со старой конфигурацией.

## `MCP_RUSSIA_TOOL_SEARCH`

Переменная управляет тем, как набор tools показывается модели:

| Значение | Поведение | Когда использовать |
|----------|-----------|--------------------|
| `bm25` | Показывает только top-N релевантных tools, meta-tools остаются доступными всегда | Базовый режим |
| `none` | Публикует весь каталог tools без фильтрации | Отладка, ручная проверка, очень большой контекст |
| `code_mode` | Экспериментальный режим discovery через `get_tags`, `search` и `GetSchemas` | Продвинутые сценарии и внутренние тесты |

## API-ключи

### Portal da Transparencia

Бесплатный ключ повышает rate limit. Без него feature `transparencia` отключается.

1. Откройте `http://portaldatransparencia.gov.br/api-de-dados/cadastrar-email`
2. Зарегистрируйте email
3. Скопируйте выданный ключ
4. Установите `TRANSPARENCIA_API_KEY=<ваш-ключ>`

### DataJud / CNJ

Бесплатный ключ дает доступ к судебным данным. Без него feature `datajud` отключается.

1. Откройте `https://datajud-wiki.cnj.jus.br/api-publica/acesso`
2. Пройдите процедуру регистрации
3. Установите `DATAJUD_API_KEY=<ваш-ключ>`

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
        "TRANSPARENCIA_API_KEY": "your-key",
        "DATAJUD_API_KEY": "your-key",
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
        "TRANSPARENCIA_API_KEY": "your-key",
        "DATAJUD_API_KEY": "your-key"
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
  -e TRANSPARENCIA_API_KEY=your-key \
  -e DATAJUD_API_KEY=your-key \
  -- uvx --from mcp-russia python -m mcp_russia.server
```

### HTTP transport

```bash
TRANSPARENCIA_API_KEY=xxx DATAJUD_API_KEY=yyy \
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

Отдельные features могут использовать общий `RateLimiter` из `src/mcp_brasil/_shared/rate_limiter.py`:

```python
limiter = RateLimiter(max_requests=5, period=1.0)

async with limiter:
    data = await http_get(url)
```
