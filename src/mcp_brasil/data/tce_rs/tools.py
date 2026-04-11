"""Tool functions for the TCE-RS feature.

Инструмент совместимости с API Счётного трибунала штата Риу-Гранди-ду-Сул (TCE-RS) Бразилии.
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
    - Использует Context для структурированного логирования и отчёта о прогрессе
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_brl, format_percent

from . import client


async def listar_municipios_rs(ctx: Context) -> str:
    """(legacy) Список муниципалитетов штата Риу-Гранди-ду-Сул, зарегистрированных в TCE-RS.

    Примечание: инструмент совместимости для бразильских данных TCE-RS.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Справочные данные портала открытых данных TCE-RS.
    Возвращает код, название и код IBGE каждого муниципалитета.

    Args:
        ctx: Контекст MCP.

    Returns:
        Список муниципалитетов RS с кодами.
    """
    await ctx.info("Buscando municípios do RS no TCE-RS...")
    municipios = await client.listar_municipios()

    if not municipios:
        return "Nenhum município encontrado no TCE-RS."

    lines: list[str] = [f"**{len(municipios)} municípios do RS no TCE-RS:**\n"]
    for m in municipios[:50]:
        ibge = f", IBGE: {m.codigo_ibge}" if m.codigo_ibge else ""
        lines.append(f"- **{m.nome or '—'}** (código: `{m.codigo}`{ibge})")

    if len(municipios) > 50:
        lines.append(f"\n*Mostrando 50 de {len(municipios)} municípios.*")
    return "\n".join(lines)


async def buscar_indices_educacao_rs(
    ctx: Context,
    ano: int,
    municipio: str | None = None,
) -> str:
    """(legacy) Поиск индексов расходов на образование муниципалитетов RS.

    Примечание: инструмент совместимости для бразильских данных TCE-RS.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные TCE-RS о соблюдении конституционного минимума 25%
    на поддержание и развитие образования (MDE). Полезно для проверки
    соблюдения муниципалитетами законодательных обязательств.

    Args:
        ctx: Контекст MCP.
        ano: Год справки (напр.: 2024).
        municipio: Фильтр по названию муниципалитета (частичный поиск).

    Returns:
        Список муниципалитетов с индексом образования.
    """
    await ctx.info(f"Buscando índices de educação no TCE-RS (ano={ano})...")
    indices = await client.buscar_indices_educacao(ano)

    if municipio:
        termo = municipio.upper()
        indices = [i for i in indices if termo in (i.nome_orgao or "").upper()]

    if not indices:
        return "Nenhum índice de educação encontrado no TCE-RS."

    lines: list[str] = [f"**{len(indices)} índices de educação ({ano}):**\n"]
    for idx in indices[:30]:
        indice_fmt = format_percent(idx.indice) if idx.indice is not None else "—"
        despesa = format_brl(idx.valor_despesa) if idx.valor_despesa else "—"
        receita = format_brl(idx.valor_receita) if idx.valor_receita else "—"
        lines.append(f"- **{idx.nome_orgao or '—'}** — Índice: {indice_fmt}")
        lines.append(f"  Despesa: {despesa} | Receita: {receita}")

    if len(indices) > 30:
        lines.append(f"\n*Mostrando 30 de {len(indices)} municípios.*")
    return "\n".join(lines)


async def buscar_indices_saude_rs(
    ctx: Context,
    ano: int,
    municipio: str | None = None,
) -> str:
    """(legacy) Поиск индексов расходов на здравоохранение муниципалитетов RS.

    Примечание: инструмент совместимости для бразильских данных TCE-RS.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные TCE-RS о соблюдении конституционного минимума 15%
    на действия и услуги общественного здравоохранения (ASPS). Полезно для проверки
    соблюдения муниципалитетами законодательных обязательств.

    Args:
        ctx: Контекст MCP.
        ano: Год справки (напр.: 2024).
        municipio: Фильтр по названию муниципалитета (частичный поиск).

    Returns:
        Список муниципалитетов с индексом здравоохранения.
    """
    await ctx.info(f"Buscando índices de saúde no TCE-RS (ano={ano})...")
    indices = await client.buscar_indices_saude(ano)

    if municipio:
        termo = municipio.upper()
        indices = [i for i in indices if termo in (i.nome_orgao or "").upper()]

    if not indices:
        return "Nenhum índice de saúde encontrado no TCE-RS."

    lines: list[str] = [f"**{len(indices)} índices de saúde ({ano}):**\n"]
    for idx in indices[:30]:
        indice_fmt = format_percent(idx.indice) if idx.indice is not None else "—"
        despesa = format_brl(idx.valor_despesa) if idx.valor_despesa else "—"
        receita = format_brl(idx.valor_receita) if idx.valor_receita else "—"
        lines.append(f"- **{idx.nome_orgao or '—'}** — Índice: {indice_fmt}")
        lines.append(f"  Despesa: {despesa} | Receita: {receita}")

    if len(indices) > 30:
        lines.append(f"\n*Mostrando 30 de {len(indices)} municípios.*")
    return "\n".join(lines)


async def buscar_gestao_fiscal_rs(
    ctx: Context,
    ano: int,
    municipio: str | None = None,
) -> str:
    """(legacy) Поиск данных фискального управления (LRF) муниципалитетов RS.

    Примечание: инструмент совместимости для бразильских данных TCE-RS.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные TCE-RS о Законе об ответственности за управление: чистый текущий доход,
    расходы на персонал, консолидированный долг, кредитные операции,
    и расходы на образование (MDE) и здравоохранение (ASPS).

    Args:
        ctx: Контекст MCP.
        ano: Год справки (напр.: 2024).
        municipio: Фильтр по названию муниципалитета (частичный поиск).

    Returns:
        Список муниципалитетов с данными фискального управления.
    """
    await ctx.info(f"Buscando gestão fiscal no TCE-RS (ano={ano})...")
    dados = await client.buscar_gestao_fiscal(ano)

    if municipio:
        termo = municipio.upper()
        dados = [d for d in dados if termo in (d.nome_orgao or "").upper()]

    if not dados:
        return "Nenhum dado de gestão fiscal encontrado no TCE-RS."

    lines: list[str] = [f"**{len(dados)} registros de gestão fiscal ({ano}):**\n"]
    for d in dados[:20]:
        rcl = format_brl(d.receita_corrente_liquida) if d.receita_corrente_liquida else "—"
        pessoal = format_brl(d.despesa_pessoal) if d.despesa_pessoal else "—"
        divida = format_brl(d.divida_consolidada) if d.divida_consolidada else "—"
        lines.append(f"### {d.nome_orgao or '—'}")
        lines.append(f"- **Receita corrente líquida:** {rcl}")
        lines.append(f"- **Despesa com pessoal:** {pessoal}")
        lines.append(f"- **Dívida consolidada:** {divida}")
        lines.append("")

    if len(dados) > 20:
        lines.append(f"*Mostrando 20 de {len(dados)} registros.*")
    return "\n".join(lines)


async def buscar_datasets_rs(
    ctx: Context,
    query: str,
    grupo: str | None = None,
    limite: int = 10,
) -> str:
    """(legacy) Поиск наборов данных на портале открытых данных TCE-RS.

    Примечание: инструмент совместимости для бразильских данных TCE-RS.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Портал CKAN TCE-RS содержит ~69 000 наборов данных, организованных в 16 групп:
    расходы, доходы, закупки, контракты, решения, образование, здравоохранение,
    социальное обеспечение, фискальное управление, омбудсмен и другие.

    Args:
        ctx: Контекст MCP.
        query: Поисковый термин (напр.: "consolidado 2024", "licitacoes recife").
        grupo: Фильтр по группе (напр.: "despesa", "licitacoes", "contratos").
        limite: Максимум результатов (1-50, по умолчанию 10).

    Returns:
        Список наборов данных с заголовком, группой и ссылкой для скачивания.
    """
    await ctx.info(f"Buscando datasets no TCE-RS (query='{query}')...")
    datasets, total = await client.buscar_datasets(query, grupo=grupo, limite=limite)

    if not datasets:
        return "Nenhum dataset encontrado no portal do TCE-RS."

    lines: list[str] = [f"**{total} datasets encontrados (mostrando {len(datasets)}):**\n"]
    for ds in datasets:
        notas = f" — {ds.notas}" if ds.notas else ""
        grupo_txt = f" [{ds.grupo}]" if ds.grupo else ""
        recursos = f" ({ds.num_recursos} recursos)" if ds.num_recursos else ""
        lines.append(f"### {ds.titulo or ds.nome or '—'}{grupo_txt}")
        lines.append(f"- **URL:** {ds.url or '—'}{recursos}")
        if notas:
            lines.append(f"- **Descrição:** {notas}")
        lines.append("")

    return "\n".join(lines)
