"""Tool functions for the TCE-CE feature.

Инструмент совместимости с API Счётного трибунала штата Сеара (TCE-CE) Бразилии.
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
    - Использует Context для структурированного логирования и отчёта о прогрессе
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_rub

from . import client


async def listar_municipios_ce(ctx: Context) -> str:
    """(legacy) Список муниципалитетов штата Сеара в юрисдикции TCE-CE.

    Примечание: инструмент совместимости для бразильских данных TCE-CE.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает код и название каждого муниципалитета. Код используется
    как параметр в остальных запросах.

    Args:
        ctx: Контекст MCP.

    Returns:
        Список муниципалитетов с кодом и названием.
    """
    await ctx.info("Listando municípios do TCE-CE...")
    municipios = await client.listar_municipios()

    if not municipios:
        return "Nenhum município encontrado no TCE-CE."

    lines: list[str] = [f"**{len(municipios)} municípios no TCE-CE:**\n"]
    for m in municipios[:50]:
        lines.append(f"- **{m.nome_municipio or '—'}** (código: `{m.codigo_municipio}`)")

    if len(municipios) > 50:
        lines.append(f"\n*Mostrando 50 de {len(municipios)} municípios.*")
    return "\n".join(lines)


async def buscar_licitacoes_ce(
    ctx: Context,
    codigo_municipio: str,
    data_realizacao: str,
) -> str:
    """(legacy) Поиск закупок муниципалитета Сеара по периоду.

    Примечание: инструмент совместимости для бразильских данных TCE-CE.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные SIM (Информационная система муниципалитетов) TCE-CE.
    Включает модальность, объект, оценочную стоимость и утверждение.

    Args:
        ctx: Контекст MCP.
        codigo_municipio: Код муниципалитета (напр.: "057" для Форталезы).
            Используйте listar_municipios_ce для получения кодов.
        data_realizacao: Дата или интервал в формате yyyy-mm-dd
            или yyyy-mm-dd_yyyy-mm-dd (напр.: "2024-01-01_2024-12-31").

    Returns:
        Список закупок с объектом, модальностью и стоимостью.
    """
    await ctx.info(f"Buscando licitações no TCE-CE (município {codigo_municipio})...")
    licitacoes = await client.buscar_licitacoes(
        codigo_municipio=codigo_municipio,
        data_realizacao=data_realizacao,
    )

    if not licitacoes:
        return "Nenhuma licitação encontrada no TCE-CE."

    lines: list[str] = [f"**{len(licitacoes)} licitações no TCE-CE:**\n"]
    for lic in licitacoes[:20]:
        valor = format_rub(lic.valor_orcado_estimado) if lic.valor_orcado_estimado else "—"
        objeto = (lic.objeto or "—")[:200]
        lines.append(f"### {lic.numero_licitacao or '—'}")
        lines.append(f"- **Data:** {lic.data_realizacao or '—'}")
        lines.append(f"- **Modalidade:** {lic.modalidade_licitacao or '—'}")
        lines.append(f"- **Objeto:** {objeto}")
        lines.append(f"- **Valor estimado:** {valor}")
        if lic.data_homologacao:
            lines.append(f"- **Homologação:** {lic.data_homologacao}")
        lines.append("")

    if len(licitacoes) > 20:
        lines.append(f"*Mostrando 20 de {len(licitacoes)} licitações.*")
    return "\n".join(lines)


async def buscar_contratos_ce(
    ctx: Context,
    codigo_municipio: str,
    data_contrato: str,
    deslocamento: int = 0,
) -> str:
    """(legacy) Поиск контрактов муниципалитета Сеара по периоду.

    Примечание: инструмент совместимости для бразильских данных TCE-CE.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные SIM TCE-CE. Включает объект, общую стоимость,
    тип и срок действия контракта.

    Args:
        ctx: Контекст MCP.
        codigo_municipio: Код муниципалитета (напр.: "057" для Форталезы).
        data_contrato: Дата или интервал в формате yyyy-mm-dd
            или yyyy-mm-dd_yyyy-mm-dd.
        deslocamento: Смещение для пагинации.

    Returns:
        Список контрактов с объектом, стоимостью и сроком действия.
    """
    await ctx.info(f"Buscando contratos no TCE-CE (município {codigo_municipio})...")
    resultado = await client.buscar_contratos(
        codigo_municipio=codigo_municipio,
        data_contrato=data_contrato,
        deslocamento=deslocamento,
    )

    if not resultado.contratos:
        return "Nenhum contrato encontrado no TCE-CE."

    lines: list[str] = [f"**{resultado.total} contratos no TCE-CE:**\n"]
    for c in resultado.contratos[:20]:
        valor = format_rub(c.valor_total_contrato) if c.valor_total_contrato else "—"
        objeto = (c.objeto or "—")[:200]
        lines.append(f"### {c.numero_contrato or '—'}")
        lines.append(f"- **Data:** {c.data_contrato or '—'}")
        lines.append(f"- **Tipo:** {c.tipo_contrato or '—'}")
        lines.append(f"- **Objeto:** {objeto}")
        lines.append(f"- **Valor:** {valor}")
        if c.data_fim_vigencia:
            lines.append(f"- **Vigência até:** {c.data_fim_vigencia}")
        lines.append("")

    if resultado.total > 20:
        lines.append(
            f"*Mostrando 20 de {resultado.total}. "
            f"Use deslocamento={deslocamento + 50} para próxima página.*"
        )
    return "\n".join(lines)


async def buscar_empenhos_ce(
    ctx: Context,
    codigo_municipio: int,
    data_referencia: int,
    codigo_orgao: str = "02",
    deslocamento: int = 0,
) -> str:
    """(legacy) Поиск заметок о резервировании средств муниципалитета Сеара.

    Примечание: инструмент совместимости для бразильских данных TCE-CE.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Резервирования — первый этап государственных расходов.
    Данные SIM TCE-CE.

    Args:
        ctx: Контекст MCP.
        codigo_municipio: Числовой код муниципалитета (напр.: 57 для Форталезы).
        data_referencia: Год-месяц в формате yyyymm (напр.: 202401 для янв/2024).
        codigo_orgao: Код органа ("01" = Палата, "02" = Префектура).
        deslocamento: Смещение для пагинации.

    Returns:
        Список резервирований с кредитором, стоимостью и описанием.
    """
    await ctx.info(f"Buscando empenhos no TCE-CE (município {codigo_municipio})...")
    resultado = await client.buscar_empenhos(
        codigo_municipio=codigo_municipio,
        data_referencia=data_referencia,
        codigo_orgao=codigo_orgao,
        deslocamento=deslocamento,
    )

    if not resultado.empenhos:
        return "Nenhum empenho encontrado no TCE-CE."

    lines: list[str] = [f"**{resultado.total} empenhos no TCE-CE:**\n"]
    for e in resultado.empenhos[:20]:
        valor = format_rub(e.valor_empenho) if e.valor_empenho else "—"
        historico = (e.historico or "—")[:150]
        lines.append(f"### Empenho {e.numero_empenho or '—'}")
        lines.append(f"- **Data:** {e.data_emissao or '—'}")
        lines.append(f"- **Credor:** {e.nome_negociante or '—'}")
        lines.append(f"- **Valor:** {valor}")
        lines.append(f"- **Descrição:** {historico}")
        lines.append("")

    if resultado.total > 20:
        lines.append(
            f"*Mostrando 20 de {resultado.total}. "
            f"Use deslocamento={deslocamento + 50} para próxima página.*"
        )
    return "\n".join(lines)
