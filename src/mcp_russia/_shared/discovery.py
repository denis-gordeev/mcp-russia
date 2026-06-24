"""Рекомендация инструментов mcp-russia на базе LLM.

Использует API Anthropic для понимания намерений пользователя и подбора
наиболее релевантных инструментов из текущего каталога сервера.
"""

from __future__ import annotations

import logging

from ..settings import ANTHROPIC_API_KEY

logger = logging.getLogger("mcp-russia.discovery")

_kesh_kataloga: str = ""


def _formatirovat_signaturu_instrumenta(imya_modulya: str, tool_name: str, tool: object) -> str:
    """Форматирование инструмента в читаемую сигнатуру с параметрами и описанием.

    Формирует вывод вида:
        - gosduma_poluchit_deputatov(familiya?: str) — Список депутатов Госдумы.

    Аргументы:
        imya_modulya: Имя модуля (префикс инструмента).
        tool_name: Имя инструмента.
        tool: Объект инструмента.
    """
    params = getattr(tool, "parameters", {})
    properties: dict[str, dict[str, object]] = params.get("properties", {})
    required: list[str] = params.get("required", [])

    param_parts: list[str] = []
    for pname, pschema in properties.items():
        if pname == "ctx":
            continue
        ptype = pschema.get("type", "any")
        opt = "" if pname in required else "?"
        param_parts.append(f"{pname}{opt}: {ptype}")

    signature = ", ".join(param_parts)
    full_name = f"{imya_modulya}_{tool_name}"

    desc = (getattr(tool, "description", "") or "").split("\n")[0]

    return f"- `{full_name}({signature})` — {desc}"


def postroit_katalog(registry: object) -> str:
    """Построение подробного каталога всех инструментов из реестра.

    Использует MetaFunktsii (имя, описание, авторизация) и схемы инструментов
    (параметры, типы, описания) для формирования детального каталога для LLM.

    Аргументы:
        registry: Экземпляр ReyestrFunktsiy с обнаруженными функциями.

    Возвращает:
        Каталог в формате Markdown с контекстом функций и сигнатурами инструментов.
    """
    global _kesh_kataloga
    if _kesh_kataloga:
        return _kesh_kataloga

    lines: list[str] = []
    features = getattr(registry, "funktsii", {})
    for feat in features.values():
        meta = feat.meta
        auth_info = (
            f"Требуется аутентификация ({meta.auth_env_var})"
            if meta.requires_auth
            else (
                f"Рекомендуется аутентификация ({meta.auth_env_var})"
                if meta.auth_env_var
                else "Без аутентификации"
            )
        )
        lines.append(f"\n## {meta.name}: {meta.description}")
        lines.append(f"Авторизация: {auth_info}")

        server = feat.server
        if hasattr(server, "_tool_manager") and hasattr(server._tool_manager, "_tools"):
            for tool_name, tool in server._tool_manager._tools.items():
                lines.append(_formatirovat_signaturu_instrumenta(meta.name, tool_name, tool))

    _kesh_kataloga = "\n".join(lines)
    return _kesh_kataloga


async def rekomendovat_instrumenty_impl(query: str, catalog: str) -> str:
    """Вызов API Anthropic для рекомендации инструментов по запросу пользователя.

    Аргументы:
        query: Вопрос пользователя на естественном языке.
        catalog: Предварительно собранный каталог всех инструментов.

    Возвращает:
        Рекомендации LLM с пояснениями.
    """
    try:
        import anthropic
    except ImportError:
        return (
            "Ошибка: пакет 'anthropic' не установлен. "
            "Установите его командой: pip install 'mcp-russia[llm]'\n\n"
            "В качестве альтернативы используйте инструмент 'search_tools'."
        )

    api_key = ANTHROPIC_API_KEY
    if not api_key:
        return (
            "Ошибка: переменная ANTHROPIC_API_KEY не настроена. "
            "Задайте ANTHROPIC_API_KEY, чтобы использовать этот мета-инструмент.\n\n"
            "В качестве альтернативы используйте инструмент 'search_tools'."
        )

    client = anthropic.AsyncAnthropic(api_key=api_key)

    system_prompt = (
        "Ты помогаешь подобрать инструменты из каталога mcp-russia. "
        "В каталоге могут встречаться исторические названия функций, "
        "сохранённые для совместимости. На основе вопроса пользователя "
        "выбери 3-5 наиболее релевантных инструментов. Для каждого:\n"
        "1. Полное имя инструмента (с префиксом функции)\n"
        "2. Почему он релевантен запросу\n"
        "3. Пример использования с основными параметрами\n\n"
        "Отвечай по-русски, кратко и по делу.\n\n"
        f"## Каталог инструментов\n{catalog}"
    )

    try:
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": query}],
        )
        block = response.content[0]
        return str(getattr(block, "text", ""))
    except Exception as e:
        logger.error("Ошибка вызова API Anthropic: %s", e)
        return (
            f"Ошибка при обращении к LLM: {e}\n\n"
            "В качестве альтернативы используйте 'search_tools'."
        )
