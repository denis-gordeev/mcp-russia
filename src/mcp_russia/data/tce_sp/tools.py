"""Tool functions for the TCE-SP feature.

Инструмент совместимости с API Счётного трибунала штата Сан-Паулу (TCE-SP) Бразилии.
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
    - Использует Context для структурированного логирования и отчёта о прогрессе
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_rub

from . import client


async def listar_municipios_sp(ctx: Context) -> str:
    """(legacy) Список 645 муниципалитетов штата Сан-Паулу в юрисдикции TCE-SP.

    Примечание: инструмент совместимости для бразильских данных TCE-SP.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает полное название и slug (используется как параметр в остальных инструментах).
    Статические данные — не меняются между запросами.

    Args:
        ctx: Контекст MCP.

    Returns:
        Список муниципалитетов с slug и полным названием.
    """
    await ctx.info("Listando municípios do TCE-SP...")
    municipios = await client.listar_municipios()

    if not municipios:
        return "Nenhum município encontrado no TCE-SP."

    lines: list[str] = [f"**{len(municipios)} municípios no TCE-SP:**\n"]
    for m in municipios[:50]:
        lines.append(f"- **{m.municipio_extenso}** (`{m.municipio}`)")

    if len(municipios) > 50:
        lines.append(f"\n*Mostrando 50 de {len(municipios)} municípios.*")
    return "\n".join(lines)


async def consultar_despesas_sp(
    ctx: Context,
    municipio: str,
    exercicio: int,
    mes: int,
) -> str:
    """(legacy) Запрос расходов муниципалитета Сан-Паулу за конкретный месяц.

    Примечание: инструмент совместимости для бразильских данных TCE-SP.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает резервирования, платежи и аннулирования с поставщиком и стоимостью.
    Данные системы Audesp TCE-SP с 2014 года.

    Args:
        ctx: Контекст MCP.
        municipio: Slug муниципалитета (напр.: "campinas", "sao-paulo").
            Используйте listar_municipios_sp для получения валидных slug.
        exercicio: Финансовый год (2014 до текущего, напр.: 2025).
        mes: Месяц (1 до 12).

    Returns:
        Список расходов с поставщиком, событием и стоимостью.
    """
    await ctx.info(f"Buscando despesas de {municipio} ({exercicio}/{mes})...")
    despesas = await client.buscar_despesas(municipio, exercicio, mes)

    if not despesas:
        return f"Nenhuma despesa encontrada para {municipio} em {mes}/{exercicio}."

    total_valor = sum(d.vl_despesa for d in despesas if d.vl_despesa and d.vl_despesa > 0)
    lines: list[str] = [
        f"**{len(despesas)} registros de despesas em {municipio} ({mes}/{exercicio}):**\n"
    ]
    if total_valor:
        lines.append(f"**Total empenhado (positivo):** {format_rub(total_valor)}\n")

    for d in despesas[:30]:
        valor = format_rub(d.vl_despesa) if d.vl_despesa else "—"
        lines.append(f"- [{d.evento or '—'}] {d.nm_fornecedor or '—'}: {valor}")
        if d.nr_empenho:
            lines[-1] += f" (empenho {d.nr_empenho})"

    if len(despesas) > 30:
        lines.append(f"\n*Mostrando 30 de {len(despesas)} registros.*")
    return "\n".join(lines)


async def consultar_receitas_sp(
    ctx: Context,
    municipio: str,
    exercicio: int,
    mes: int,
) -> str:
    """(legacy) Запрос доходов муниципалитета Сан-Паулу за конкретный месяц.

    Примечание: инструмент совместимости для бразильских данных TCE-SP.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает сборы по источнику ресурсов, алинее и субалинее.
    Данные системы Audesp TCE-SP с 2014 года.

    Args:
        ctx: Контекст MCP.
        municipio: Slug муниципалитета (напр.: "campinas", "sao-paulo").
            Используйте listar_municipios_sp для получения валидных slug.
        exercicio: Финансовый год (2014 до текущего, напр.: 2025).
        mes: Месяц (1 до 12).

    Returns:
        Список доходов с источником, классификацией и стоимостью.
    """
    await ctx.info(f"Buscando receitas de {municipio} ({exercicio}/{mes})...")
    receitas = await client.buscar_receitas(municipio, exercicio, mes)

    if not receitas:
        return f"Nenhuma receita encontrada para {municipio} em {mes}/{exercicio}."

    total_arrecadado = sum(r.vl_arrecadacao for r in receitas if r.vl_arrecadacao)
    lines: list[str] = [
        f"**{len(receitas)} registros de receitas em {municipio} ({mes}/{exercicio}):**\n"
    ]
    if total_arrecadado:
        lines.append(f"**Total arrecadado:** {format_rub(total_arrecadado)}\n")

    for r in receitas[:30]:
        valor = format_rub(r.vl_arrecadacao) if r.vl_arrecadacao else "—"
        alinea = r.ds_alinea or "—"
        fonte = r.ds_fonte_recurso or "—"
        lines.append(f"- **{alinea}**: {valor}")
        lines.append(f"  Fonte: {fonte}")

    if len(receitas) > 30:
        lines.append(f"\n*Mostrando 30 de {len(receitas)} registros.*")
    return "\n".join(lines)
