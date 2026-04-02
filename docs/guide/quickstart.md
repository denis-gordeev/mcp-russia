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
        "TRANSPARENCIA_API_KEY": "your-key-here",
        "DATAJUD_API_KEY": "your-key-here"
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
        "TRANSPARENCIA_API_KEY": "your-key-here",
        "DATAJUD_API_KEY": "your-key-here"
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

На этапе миграции ответы все еще могут ссылаться на исторические feature-имена и бразильские датасеты. Это связано с тем, что внутреннее дерево `mcp_brasil` пока не заменено полностью.

## Ключи API

Часть интеграций работает без ключей, а часть использует legacy-настройки исходного проекта. Для переходного периода ориентируйтесь на:

| Переменная | Назначение |
|------------|------------|
| `TRANSPARENCIA_API_KEY` | Доступ к legacy-интеграции Portal da Transparência |
| `DATAJUD_API_KEY` | Доступ к legacy-интеграции DataJud/CNJ |

## Важно про совместимость

- Для установки и запуска используйте `mcp-russia` и `mcp_russia`.
- Для внутренних импортов и части тестов в кодовой базе пока остается `mcp_brasil`.
- Это не конфликт, а сознательный переходный слой.

## Дальше

Если вы хотите разрабатывать сервер, переходите к [разделу по разработке](development.md) и [архитектуре](../concepts/architecture.md).
