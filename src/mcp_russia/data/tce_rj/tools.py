"""Tool functions for the TCE-RJ feature.

Инструмент совместимости с API Счётного трибунала штата Рио-де-Жанейро (TCE-RJ) Бразилии.
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


async def buscar_licitacoes(
    ctx: Context,
    ano: int | None = None,
    municipio: str | None = None,
    inicio: int = 0,
    limite: int = 50,
) -> str:
    """(legacy) Поиск муниципальных закупок штата Рио-де-Жанейро.

    Примечание: инструмент совместимости для бразильских данных TCE-RJ.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные конкурсных процедур 92 муниципалитетов штата Рио-де-Жанейро,
    включая модальность, объект, оценочную стоимость и статус.

    Args:
        ctx: Контекст MCP.
        ano: Год справки (напр.: 2024).
        municipio: Название муниципалитета ЗАГЛАВНЫМИ (напр.: "NITEROI").
        inicio: Смещение для пагинации.
        limite: Максимальное количество результатов.

    Returns:
        Список закупок с объектом, модальностью и стоимостью.
    """
    await ctx.info("Buscando licitações no TCE-RJ...")
    resultado = await client.buscar_licitacoes(
        ano=ano, municipio=municipio, inicio=inicio, limite=limite
    )

    if not resultado.licitacoes:
        return "Nenhuma licitação encontrada no TCE-RJ."

    lines: list[str] = [f"**{resultado.total} licitações no TCE-RJ:**\n"]
    for lic in resultado.licitacoes[:20]:
        valor = format_rub(lic.valor_estimado) if lic.valor_estimado else "—"
        lines.append(f"### {lic.numero_edital or lic.processo_licitatorio or '—'}")
        lines.append(f"- **Município:** {lic.ente or '—'}")
        lines.append(f"- **Modalidade:** {lic.modalidade or '—'}")
        lines.append(f"- **Objeto:** {lic.objeto or '—'}")
        lines.append(f"- **Valor estimado:** {valor}")
        if lic.data_homologacao:
            lines.append(f"- **Homologação:** {lic.data_homologacao}")
        lines.append("")

    if resultado.total > 20:
        lines.append(
            f"*Mostrando 20 de {resultado.total}. "
            f"Use inicio={inicio + limite} para próxima página.*"
        )
    return "\n".join(lines)


async def buscar_contratos_municipio(
    ctx: Context,
    ano: int | None = None,
    municipio: str | None = None,
    inicio: int = 0,
    limite: int = 50,
) -> str:
    """(legacy) Поиск муниципальных контрактов штата Рио-де-Жанейро.

    Примечание: инструмент совместимости для бразильских данных TCE-RJ.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Контракты, заключённые 92 муниципалитетами штата Рио-де-Жанейро с поставщиками,
    включая стоимость, срок действия и объект контракта.

    Args:
        ctx: Контекст MCP.
        ano: Год контракта (напр.: 2024).
        municipio: Название муниципалитета ЗАГЛАВНЫМИ (напр.: "NITEROI").
        inicio: Смещение для пагинации.
        limite: Максимальное количество результатов.

    Returns:
        Список контрактов с поставщиком, объектом и стоимостью.
    """
    await ctx.info("Buscando contratos municipais no TCE-RJ...")
    resultado = await client.buscar_contratos_municipio(
        ano=ano, municipio=municipio, inicio=inicio, limite=limite
    )

    if not resultado.contratos:
        return "Nenhum contrato municipal encontrado no TCE-RJ."

    lines: list[str] = [f"**{resultado.total} contratos municipais no TCE-RJ:**\n"]
    for c in resultado.contratos[:20]:
        valor = format_rub(c.valor_contrato) if c.valor_contrato else "—"
        lines.append(f"### {c.numero_contrato or '—'} ({c.ano_contrato or '—'})")
        lines.append(f"- **Município:** {c.ente or '—'}")
        lines.append(f"- **Contratado:** {c.contratado or '—'}")
        lines.append(f"- **Objeto:** {c.objeto or '—'}")
        lines.append(f"- **Valor:** {valor}")
        lines.append(f"- **Tipo:** {c.tipo_contrato or '—'}")
        lines.append("")

    if resultado.total > 20:
        lines.append(
            f"*Mostrando 20 de {resultado.total}. "
            f"Use inicio={inicio + limite} para próxima página.*"
        )
    return "\n".join(lines)


async def buscar_compras_diretas(
    ctx: Context,
    ano: int | None = None,
    municipio: str | None = None,
    inicio: int = 0,
    limite: int = 50,
) -> str:
    """(legacy) Поиск прямых закупок (отказы и необязательности) в штате Рио-де-Жанейро.

    Примечание: инструмент совместимости для бразильских данных TCE-RJ.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Закупки без торгов муниципалитетов штата Рио-де-Жанейро, включая
    отказы от торгов и необязательности с правовым обоснованием.

    Args:
        ctx: Контекст MCP.
        ano: Год справки.
        municipio: Название муниципалитета ЗАГЛАВНЫМИ (напр.: "NITEROI").
        inicio: Смещение для пагинации.
        limite: Максимальное количество результатов.

    Returns:
        Список прямых закупок с поставщиком и стоимостью.
    """
    await ctx.info("Buscando compras diretas municipais no TCE-RJ...")
    compras = await client.buscar_compras_diretas_municipio(
        ano=ano, municipio=municipio, inicio=inicio, limite=limite
    )

    if not compras:
        return "Nenhuma compra direta encontrada no TCE-RJ."

    lines: list[str] = [f"**{len(compras)} compras diretas no TCE-RJ:**\n"]
    for c in compras[:20]:
        valor = format_rub(c.valor_processo) if c.valor_processo else "—"
        lines.append(f"### Processo {c.processo or '—'}")
        lines.append(f"- **Unidade:** {c.unidade or '—'}")
        lines.append(f"- **Objeto:** {c.objeto or '—'}")
        lines.append(f"- **Fornecedor:** {c.fornecedor_vencedor or '—'}")
        lines.append(f"- **Valor:** {valor}")
        lines.append(f"- **Fundamentação:** {c.afastamento or '—'}")
        lines.append("")

    return "\n".join(lines)


async def buscar_obras_paralisadas(ctx: Context) -> str:
    """(legacy) Поиск приостановленных общественных работ штата Рио-де-Жанейро.

    Примечание: инструмент совместимости для бразильских данных TCE-RJ.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Список всех приостановленных работ (штатных и муниципальных) с
    указанием причины приостановки, времени простоя, стоимости контракта и статуса.
    Фундаментальные данные для контроля инвестиций.

    Args:
        ctx: Контекст MCP.

    Returns:
        Список приостановленных работ с причиной и стоимостью.
    """
    await ctx.info("Buscando obras paralisadas no TCE-RJ...")
    obras = await client.buscar_obras_paralisadas()

    if not obras:
        return "Nenhuma obra paralisada encontrada no TCE-RJ."

    lines: list[str] = [f"**{len(obras)} obras paralisadas no RJ:**\n"]
    for o in obras[:20]:
        valor = format_rub(o.valor_total_contrato) if o.valor_total_contrato else "—"
        lines.append(f"### {o.nome or '—'}")
        lines.append(f"- **Ente:** {o.ente or '—'} ({o.tipo_ente or '—'})")
        lines.append(f"- **Função:** {o.funcao_governo or '—'}")
        lines.append(f"- **Contratada:** {o.nome_contratada or '—'}")
        lines.append(f"- **Valor contrato:** {valor}")
        lines.append(f"- **Tempo parado:** {o.tempo_paralisacao or '—'}")
        lines.append(f"- **Motivo:** {o.motivo_paralisacao or '—'}")
        lines.append(f"- **Status:** {o.status_contrato or '—'}")
        lines.append("")

    if len(obras) > 20:
        lines.append(f"*Mostrando 20 de {len(obras)} obras paralisadas.*")
    return "\n".join(lines)


async def buscar_penalidades(
    ctx: Context,
    tipo: str | None = None,
) -> str:
    """(legacy) Поиск штрафов и возмещений, наложенных TCE-RJ на муниципалитеты.

    Примечание: инструмент совместимости для бразильских данных TCE-RJ.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Штрафы и долги, наложенные Счётным трибуналом на муниципальных
    управленцев за нарушения в управлении.

    Args:
        ctx: Контекст MCP.
        tipo: Тип штрафа: "multa" или "debito".

    Returns:
        Список штрафов со стоимостью и процессами.
    """
    await ctx.info("Buscando penalidades no TCE-RJ...")
    penalidades = await client.buscar_penalidades(tipo=tipo)

    if not penalidades:
        return "Nenhuma penalidade encontrada no TCE-RJ."

    lines: list[str] = [f"**{len(penalidades)} penalidades no TCE-RJ:**\n"]
    for p in penalidades[:20]:
        valor = format_rub(p.valor_penalidade) if p.valor_penalidade else "—"
        lines.append(f"### {p.condenacao or '—'} ({p.ano_condenacao or '—'})")
        lines.append(f"- **Município:** {p.ente or '—'}")
        lines.append(f"- **Órgão:** {p.nome_orgao or '—'}")
        lines.append(f"- **Valor:** {valor}")
        lines.append(f"- **Natureza:** {p.grupo_natureza or '—'}")
        lines.append(f"- **Processo:** {p.processo or '—'}")
        lines.append("")

    if len(penalidades) > 20:
        lines.append(f"*Mostrando 20 de {len(penalidades)} penalidades.*")
    return "\n".join(lines)


async def buscar_prestacao_contas(ctx: Context) -> str:
    """(legacy) Поиск отчётов о расходовании средств муниципалитетов штата Рио-де-Жанейро.

    Примечание: инструмент совместимости для бразильских данных TCE-RJ.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Результат анализа счетов мэров TCE-RJ,
    указывающий благоприятное или неблагоприятное заключение.

    Args:
        ctx: Контекст MCP.

    Returns:
        Список муниципалитетов с индикатором отчётности.
    """
    await ctx.info("Buscando prestação de contas no TCE-RJ...")
    contas = await client.buscar_prestacao_contas()

    if not contas:
        return "Nenhuma prestação de contas encontrada."

    lines: list[str] = [f"**{len(contas)} prestações de contas no TCE-RJ:**\n"]
    for c in contas[:30]:
        lines.append(
            f"- **{c.municipio or '—'}** ({c.ano or '—'}): "
            f"{c.indicador or '—'} — {c.responsavel or '—'}"
        )

    if len(contas) > 30:
        lines.append(f"\n*Mostrando 30 de {len(contas)} registros.*")
    return "\n".join(lines)


async def buscar_concessoes(
    ctx: Context,
    municipio: str | None = None,
) -> str:
    """(legacy) Поиск муниципальных концессий штата Рио-де-Жанейро.

    Примечание: инструмент совместимости для бразильских данных TCE-RJ.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    ГЧП, концессии транспорта, общественного освещения, водоснабжения и канализации,
    а также остальные делегированные общественные услуги муниципалитетов штата.

    Args:
        ctx: Контекст MCP.
        municipio: Название муниципалитета для фильтрации (ЗАГЛАВНЫМИ).

    Returns:
        Список концессий с концессионером, объектом и стоимостью.
    """
    await ctx.info("Buscando concessões públicas no TCE-RJ...")
    dados = await client.buscar_concessoes()

    if municipio:
        dados = [d for d in dados if d.municipio.upper() == municipio.upper()]

    if not dados:
        return "Nenhuma concessão encontrada no TCE-RJ."

    total_concessoes = sum(len(d.concessoes) for d in dados)
    lines: list[str] = [f"**{total_concessoes} concessões em {len(dados)} municípios:**\n"]
    count = 0
    for mun in dados:
        if count >= 20:
            break
        for c in mun.concessoes:
            if count >= 20:
                break
            valor = format_rub(c.valor_total_outorga) if c.valor_total_outorga else "—"
            lines.append(f"### {c.numero or '—'} — {mun.municipio}")
            lines.append(f"- **Objeto:** {c.objeto or '—'}")
            lines.append(f"- **Concessionário:** {c.nome_razao_social or '—'}")
            lines.append(f"- **Natureza:** {c.natureza or '—'}")
            lines.append(f"- **Situação:** {c.situacao_concessao or '—'}")
            lines.append(f"- **Outorga:** {valor}")
            lines.append("")
            count += 1

    if total_concessoes > 20:
        lines.append(f"*Mostrando 20 de {total_concessoes} concessões.*")
    return "\n".join(lines)
