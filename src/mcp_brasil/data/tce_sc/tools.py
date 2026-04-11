"""Tool functions for the TCE-SC feature.

Инструмент совместимости с API Счётного трибунала штата Санта-Катарина (TCE-SC) Бразилии.
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
    - Использует Context для структурированного логирования и отчёта о прогрессе
"""

from __future__ import annotations

from fastmcp import Context

from . import client


async def listar_municipios_sc(ctx: Context) -> str:
    """(legacy) Список муниципалитетов штата Санта-Катарина, зарегистрированных в TCE-SC.

    Примечание: инструмент совместимости для бразильских данных TCE-SC.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Справочные данные портала прозрачности TCE-SC.
    Возвращает код IBGE и название каждого муниципалитета.

    Args:
        ctx: Контекст MCP.

    Returns:
        Список муниципалитетов SC с кодом IBGE.
    """
    await ctx.info("Buscando municípios de SC no TCE-SC...")
    municipios = await client.listar_municipios()

    if not municipios:
        return "Nenhum município encontrado no TCE-SC."

    lines: list[str] = [f"**{len(municipios)} municípios de SC no TCE-SC:**\n"]
    for m in municipios[:50]:
        lines.append(f"- **{m.nome_municipio or '—'}** (IBGE: `{m.codigo_municipio}`)")

    if len(municipios) > 50:
        lines.append(f"\n*Mostrando 50 de {len(municipios)} municípios.*")
    return "\n".join(lines)


async def listar_unidades_gestoras_sc(
    ctx: Context,
    municipio: str | None = None,
) -> str:
    """(legacy) Список управляющих единиц штата Санта-Катарина в TCE-SC.

    Примечание: инструмент совместимости для бразильских данных TCE-SC.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Включает префектуры, палаты, автаркии, консорциумы и органы штата.
    Можно фильтровать по названию муниципалитета.

    Args:
        ctx: Контекст MCP.
        municipio: Фильтр по названию муниципалитета (частичный поиск).

    Returns:
        Список управляющих единиц с кодом, названием и муниципалитетом.
    """
    await ctx.info("Buscando unidades gestoras de SC no TCE-SC...")
    unidades = await client.listar_unidades_gestoras()

    if municipio:
        termo = municipio.upper()
        unidades = [u for u in unidades if termo in (u.nome_municipio or "").upper()]

    if not unidades:
        return "Nenhuma unidade gestora encontrada no TCE-SC."

    lines: list[str] = [f"**{len(unidades)} unidades gestoras no TCE-SC:**\n"]
    for u in unidades[:30]:
        sigla = f" ({u.sigla_unidade})" if u.sigla_unidade else ""
        lines.append(
            f"- **{u.nome_unidade or '—'}**{sigla} "
            f"(código: `{u.codigo_unidade}`, município: {u.nome_municipio or '—'})"
        )

    if len(unidades) > 30:
        lines.append(f"\n*Mostrando 30 de {len(unidades)} unidades.*")
    return "\n".join(lines)
