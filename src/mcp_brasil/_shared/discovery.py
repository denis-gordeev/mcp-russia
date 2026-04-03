"""LLM-powered tool recommendation for mcp-russia.

Uses the Anthropic API to understand user intent and recommend the most
relevant tools from the current server catalog, including legacy features
that are still exposed for compatibility.
"""

from __future__ import annotations

import logging

from ..settings import ANTHROPIC_API_KEY

logger = logging.getLogger("mcp-russia.discovery")

# Catalog is built once and cached at module level
_catalog_cache: str = ""


def _format_tool_signature(feature_name: str, tool_name: str, tool: object) -> str:
    """Format a tool as a readable signature with params and description.

    Produces output like:
        - camara_listar_deputados(nome?: str, siglaUf?: str) — Lista deputados federais.
    """
    params = getattr(tool, "parameters", {})
    properties: dict[str, dict[str, object]] = params.get("properties", {})
    required: list[str] = params.get("required", [])

    # Build param list: "nome: str" or "nome?: str" for optional
    param_parts: list[str] = []
    for pname, pschema in properties.items():
        if pname == "ctx":
            continue
        ptype = pschema.get("type", "any")
        opt = "" if pname in required else "?"
        param_parts.append(f"{pname}{opt}: {ptype}")

    signature = ", ".join(param_parts)
    full_name = f"{feature_name}_{tool_name}"

    # Use first line of description as summary
    desc = (getattr(tool, "description", "") or "").split("\n")[0]

    return f"- `{full_name}({signature})` — {desc}"


def build_catalog(registry: object) -> str:
    """Build a rich text catalog of all tools from the registry.

    Uses FeatureMeta (name, description, auth) and tool schemas (params,
    types, descriptions) to produce a detailed catalog for LLM consumption.

    Args:
        registry: FeatureRegistry instance with discovered features.

    Returns:
        Markdown-formatted catalog with feature context and tool signatures.
    """
    global _catalog_cache
    if _catalog_cache:
        return _catalog_cache

    lines: list[str] = []
    features = getattr(registry, "features", {})
    for feat in features.values():
        meta = feat.meta
        auth_info = (
            f"Requer autenticação ({meta.auth_env_var})"
            if meta.requires_auth
            else "Sem autenticação"
        )
        lines.append(f"\n## {meta.name}: {meta.description}")
        lines.append(f"Auth: {auth_info}")

        # Get tools from the feature's server
        server = feat.server
        if hasattr(server, "_tool_manager") and hasattr(server._tool_manager, "_tools"):
            for tool_name, tool in server._tool_manager._tools.items():
                lines.append(_format_tool_signature(meta.name, tool_name, tool))

    _catalog_cache = "\n".join(lines)
    return _catalog_cache


async def recomendar_tools_impl(query: str, catalog: str) -> str:
    """Call Anthropic API to recommend tools based on user query.

    Args:
        query: Natural language question from the user.
        catalog: Pre-built catalog string of all tools.

    Returns:
        LLM-generated recommendations with explanations.
    """
    try:
        import anthropic
    except ImportError:
        return (
            "Erro / Ошибка: пакет 'anthropic' не установлен. "
            "Установите его командой: pip install 'mcp-russia[llm]'\n\n"
            "В качестве альтернативы используйте tool 'search_tools'."
        )

    api_key = ANTHROPIC_API_KEY
    if not api_key:
        return (
            "Erro / Ошибка: переменная ANTHROPIC_API_KEY не настроена. "
            "Задайте ANTHROPIC_API_KEY, чтобы использовать этот meta-tool.\n\n"
            "В качестве альтернативы используйте tool 'search_tools'."
        )

    client = anthropic.AsyncAnthropic(api_key=api_key)

    system_prompt = (
        "Ты помогаешь подобрать tools из каталога mcp-russia. "
        "В каталоге могут встречаться исторические названия features, "
        "сохраненные для совместимости. На основе вопроса пользователя "
        "выбери 3-5 наиболее релевантных tools. Для каждой tool:\n"
        "1. Nome completo da tool (com prefixo da feature)\n"
        "2. Почему она релевантна запросу\n"
        "3. Пример использования с основными параметрами\n\n"
        "Отвечай по-русски, кратко и по делу.\n\n"
        f"## Каталог tools\n{catalog}"
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
        logger.error("Anthropic API call failed: %s", e)
        return (
            f"Erro / Ошибка при обращении к LLM: {e}\n\n"
            "В качестве альтернативы используйте 'search_tools'."
        )
