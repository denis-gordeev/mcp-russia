# Конфигурация

## Переменные окружения

### API-ключи

| Переменная | По умолчанию | Описание |
|----------|---------|-----------|
| `TRANSPARENCIA_API_KEY` | — | Ключ Portal da Transparencia; пока это историческая интеграция исходного проекта |
| `DATAJUD_API_KEY` | — | Ключ DataJud/CNJ; пока это историческая интеграция исходного проекта |
| `ANTHROPIC_API_KEY` | — | Нужен для `recomendar_tools` и `planejar_consulta` |

### Настройки сервера

| Переменная | По умолчанию | Описание |
|----------|---------|-----------|
| `MCP_RUSSIA_TOOL_SEARCH` | `bm25` | Режим discovery для tools |
| `MCP_RUSSIA_HTTP_TIMEOUT` | `30.0` | HTTP timeout в секундах |
| `MCP_RUSSIA_HTTP_MAX_RETRIES` | `3` | Максимум повторных попыток |

Исторические алиасы `MCP_BRASIL_*` пока тоже поддерживаются для совместимости.

### `MCP_RUSSIA_TOOL_SEARCH`

Определяет, как tools публикуются для LLM:

| Значение | Поведение | Когда использовать |
|-------|---------------|-------------|
| `bm25` | Оставляет top-10 по контексту; meta-tools всегда видимы | Режим по умолчанию |
| `none` | Показывает все tools без фильтрации | Отладка или большой контекст |
| `code_mode` | Экспериментальный discovery через `get_tags`, `search`, `GetSchemas` | Продвинутые сценарии и тесты |

## API-ключи

### Portal da Transparencia

Бесплатный ключ, который повышает rate limit. Без него feature `transparencia` отключена.

1. Acesse [portaldatransparencia.gov.br/api-de-dados/cadastrar-email](http://portaldatransparencia.gov.br/api-de-dados/cadastrar-email)
2. Cadastre seu email
3. Copie a chave recebida
4. Configure: `TRANSPARENCIA_API_KEY=sua-chave`

### DataJud / CNJ

Бесплатный ключ для доступа к судебным данным. Без него feature `datajud` отключена.

1. Acesse [datajud-wiki.cnj.jus.br/api-publica/acesso](https://datajud-wiki.cnj.jus.br/api-publica/acesso)
2. Siga o processo de cadastro
3. Configure: `DATAJUD_API_KEY=sua-chave`

### Anthropic API

Нужен только для meta-tools `recomendar_tools` и `planejar_consulta`. Без него эти tools вернут ошибку, остальные продолжают работать.

Configure: `ANTHROPIC_API_KEY=sua-chave`

## Настройка по клиентам

### Claude Desktop

```json
{
  "mcpServers": {
    "mcp-russia": {
      "command": "uvx",
      "args": ["--from", "mcp-russia", "python", "-m", "mcp_russia.server"],
      "env": {
        "TRANSPARENCIA_API_KEY": "sua-chave",
        "DATAJUD_API_KEY": "sua-chave",
        "ANTHROPIC_API_KEY": "sua-chave",
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
        "TRANSPARENCIA_API_KEY": "sua-chave",
        "DATAJUD_API_KEY": "sua-chave"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add mcp-russia -- uvx --from mcp-russia python -m mcp_russia.server
```

Для добавления env vars:

```bash
claude mcp add mcp-russia \
  -e TRANSPARENCIA_API_KEY=sua-chave \
  -e DATAJUD_API_KEY=sua-chave \
  -- uvx --from mcp-russia python -m mcp_russia.server
```

### HTTP

```bash
TRANSPARENCIA_API_KEY=xxx DATAJUD_API_KEY=yyy \
  fastmcp run mcp_russia.server:mcp --transport http --port 8000
```

## HTTP-клиент

Общий `httpx` client имеет настраиваемое поведение:

### Retry с backoff

Повтор выполняется автоматически при:
- **429** — Too Many Requests (с учетом `Retry-After`)
- **5xx** — server errors (`502`, `503`, `504`)
- **Timeout** — если API отвечает дольше `MCP_RUSSIA_HTTP_TIMEOUT`
- **Ошибках соединения** — network unreachable, DNS failure

Экспоненциальный backoff: `1s -> 2s -> 4s` (с jitter), до `MCP_RUSSIA_HTTP_MAX_RETRIES` попыток.

### Rate limiting

Каждая feature может использовать `RateLimiter` из `_shared/rate_limiter.py`:

```python
limiter = RateLimiter(max_requests=5, period=1.0)  # 5 req/s

async with limiter:
    data = await http_get(url)
```
