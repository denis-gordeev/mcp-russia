# Быстрый старт

## Установка

```bash
pip install mcp-russia
```

или через `uv`:

```bash
uv add mcp-russia
```

## Подключение к MCP-клиенту

### Claude Desktop

Добавьте в `claude_desktop_config.json`:

```json
{
  "mcpServers": {
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

### VS Code / Cursor

Создайте `.vscode/mcp.json` в корне проекта:

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

### HTTP / streamable HTTP

```bash
fastmcp run mcp_russia.server:mcp --transport http --port 8000
# сервер будет доступен на http://localhost:8000/mcp
```

или из репозитория:

```bash
make serve
```

## Проверка запуска

После подключения сервера проверьте простые запросы на естественном языке:

> "Какие интеграции сейчас активны в этом сервере?"

> "Покажи доступные инструменты для парламентских и бюджетных данных."

> "Составь план запроса для анализа расходов ведомства по нескольким источникам."

Российские модули данных (ЦБ РФ, Росстат, Госдума и др.) возвращают структурированные ответы на русском языке.

## Ключи API

Часть интеграций работает без ключей, а часть требует аутентификации:

| Переменная | Назначение |
|------------|------------|
| `ANTHROPIC_API_KEY` | Нужен для meta-tools `rekomendovat_instrumenty` и `splanirovat_zapros` |

## Совместимость

- Для установки и запуска используйте `mcp-russia` и `mcp_russia`.
- Переменные окружения используют формат `MCP_RUSSIA_*`.

## Дальше

Если вы хотите разрабатывать сервер, переходите к [разделу по разработке](development.md) и [архитектуре](../concepts/architecture.md).
