"""Tool functions for the TCE-RN feature.

Инструмент совместимости с API Счётного трибунала штата Риу-Гранди-ду-Норти (TCE-RN) Бразилии.
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


async def listar_jurisdicionados_rn(ctx: Context) -> str:
    """(legacy) Список подведомственных образований TCE-RN.

    Примечание: инструмент совместимости для бразильских данных TCE-RN.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные системы SIAI TCE-RN. Возвращает идентификатор единицы,
    необходимый для остальных запросов (расходы, доходы, закупки).

    Args:
        ctx: Контекст MCP.

    Returns:
        Список образований с идентификатором, названием и CNPJ.
    """
    await ctx.info("Buscando jurisdicionados do TCE-RN...")
    entidades = await client.listar_jurisdicionados()

    if not entidades:
        return "Nenhuma entidade jurisdicionada encontrada no TCE-RN."

    lines: list[str] = [f"**{len(entidades)} jurisdicionados no TCE-RN:**\n"]
    for e in entidades[:50]:
        cnpj = f", CNPJ: `{e.cnpj}`" if e.cnpj else ""
        lines.append(f"- **{e.nome_orgao or '—'}** (id: `{e.identificador_unidade}`{cnpj})")

    if len(entidades) > 50:
        lines.append(f"\n*Mostrando 50 de {len(entidades)} entidades.*")
    return "\n".join(lines)


async def buscar_despesas_rn(
    ctx: Context,
    ano: int,
    bimestre: int,
    id_unidade: int,
) -> str:
    """(legacy) Поиск бюджетных расходов единицы в TCE-RN.

    Примечание: инструмент совместимости для бразильских данных TCE-RN.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные бюджетного баланса (Приложение 01) со значениями ассигнований,
    резервирований, ликвидации и платежей по элементу расходов.

    Args:
        ctx: Контекст MCP.
        ano: Год справки (напр.: 2024).
        bimestre: Двухмесячный период (1-6).
        id_unidade: ID единицы (получен через listar_jurisdicionados_rn).

    Returns:
        Список расходов со значениями по элементу.
    """
    await ctx.info(f"Buscando despesas no TCE-RN (ano={ano}, bim={bimestre})...")
    despesas = await client.buscar_despesas(ano=ano, bimestre=bimestre, id_unidade=id_unidade)

    if not despesas:
        return "Nenhuma despesa encontrada no TCE-RN."

    lines: list[str] = [f"**{len(despesas)} itens de despesa:**\n"]
    for d in despesas[:20]:
        empenhado = format_rub(d.valor_empenho_ate_periodo) if d.valor_empenho_ate_periodo else "—"
        pago = format_rub(d.valor_pago_ate_periodo) if d.valor_pago_ate_periodo else "—"
        lines.append(f"- **{d.descricao_elemento_despesa or '—'}**")
        lines.append(f"  Empenhado: {empenhado} | Pago: {pago}")

    if len(despesas) > 20:
        lines.append(f"\n*Mostrando 20 de {len(despesas)} itens.*")
    return "\n".join(lines)


async def buscar_receitas_rn(
    ctx: Context,
    ano: int,
    bimestre: int,
    id_unidade: int,
) -> str:
    """(legacy) Поиск бюджетных доходов единицы в TCE-RN.

    Примечание: инструмент совместимости для бразильских данных TCE-RN.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные бюджетного баланса (Приложение 01) с прогнозируемыми
    и реализованными значениями по природе дохода.

    Args:
        ctx: Контекст MCP.
        ano: Год справки (напр.: 2024).
        bimestre: Двухмесячный период (1-6).
        id_unidade: ID единицы (получен через listar_jurisdicionados_rn).

    Returns:
        Список доходов с прогнозируемыми и реализованными значениями.
    """
    await ctx.info(f"Buscando receitas no TCE-RN (ano={ano}, bim={bimestre})...")
    receitas = await client.buscar_receitas(ano=ano, bimestre=bimestre, id_unidade=id_unidade)

    if not receitas:
        return "Nenhuma receita encontrada no TCE-RN."

    lines: list[str] = [f"**{len(receitas)} itens de receita:**\n"]
    for r in receitas[:20]:
        previsto = format_rub(r.valor_previsto_atualizado) if r.valor_previsto_atualizado else "—"
        realizado = (
            format_rub(r.valor_realizado_no_exercicio) if r.valor_realizado_no_exercicio else "—"
        )
        lines.append(f"- **{r.descricao_receita or '—'}**")
        lines.append(f"  Previsto: {previsto} | Realizado: {realizado}")

    if len(receitas) > 20:
        lines.append(f"\n*Mostrando 20 de {len(receitas)} itens.*")
    return "\n".join(lines)


async def buscar_licitacoes_rn(
    ctx: Context,
    id_unidade: int,
    data_inicio: str,
    data_fim: str,
) -> str:
    """(legacy) Поиск общественных закупок единицы в TCE-RN.

    Примечание: инструмент совместимости для бразильских данных TCE-RN.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные Приложения 38 SIAI. Требует ID единицы (получен через
    listar_jurisdicionados_rn) и период дат.

    Args:
        ctx: Контекст MCP.
        id_unidade: ID подведомственной единицы.
        data_inicio: Начальная дата (формат yyyy-MM-dd, напр.: "2024-01-01").
        data_fim: Конечная дата (формат yyyy-MM-dd, напр.: "2024-12-31").

    Returns:
        Список закупок с модальностью, объектом и стоимостью.
    """
    await ctx.info(f"Buscando licitações no TCE-RN (unidade={id_unidade})...")
    licitacoes = await client.buscar_licitacoes(
        id_unidade=id_unidade, data_inicio=data_inicio, data_fim=data_fim
    )

    if not licitacoes:
        return "Nenhuma licitação encontrada no TCE-RN."

    lines: list[str] = [f"**{len(licitacoes)} licitações no TCE-RN:**\n"]
    for lic in licitacoes[:20]:
        valor = format_rub(lic.valor_total_orcado) if lic.valor_total_orcado else "—"
        objeto = (lic.descricao_objeto or "—")[:200]
        lines.append(f"### {lic.numero_licitacao or '—'}/{lic.ano_licitacao or '—'}")
        lines.append(f"- **Modalidade:** {lic.modalidade or '—'}")
        lines.append(f"- **Objeto:** {objeto}")
        lines.append(f"- **Valor orçado:** {valor}")
        lines.append(f"- **Situação:** {lic.situacao or '—'}")
        lines.append("")

    if len(licitacoes) > 20:
        lines.append(f"*Mostrando 20 de {len(licitacoes)} licitações.*")
    return "\n".join(lines)


async def buscar_contratos_rn(
    ctx: Context,
    id_unidade: int,
    considerar_hierarquia: bool = False,
) -> str:
    """(legacy) Поиск контрактов единицы в TCE-RN.

    Примечание: инструмент совместимости для бразильских данных TCE-RN.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные Приложения 13 SIAI. Включает объект, стоимость, подрядчика
    и срок действия. Используйте considerar_hierarquia=True для включения под-органов.

    Args:
        ctx: Контекст MCP.
        id_unidade: ID подведомственной единицы.
        considerar_hierarquia: Включить под-органы (по умолчанию: False).

    Returns:
        Список контрактов с объектом, стоимостью и подрядчиком.
    """
    await ctx.info(f"Buscando contratos no TCE-RN (unidade={id_unidade})...")
    contratos = await client.buscar_contratos(
        id_unidade=id_unidade, considerar_hierarquia=considerar_hierarquia
    )

    if not contratos:
        return "Nenhum contrato encontrado no TCE-RN."

    lines: list[str] = [f"**{len(contratos)} contratos no TCE-RN:**\n"]
    for c in contratos[:20]:
        valor = format_rub(c.valor_contrato) if c.valor_contrato else "—"
        objeto = (c.objeto_contrato or "—")[:200]
        lines.append(f"### Contrato {c.numero_contrato or '—'}/{c.ano_contrato or '—'}")
        lines.append(f"- **Contratado:** {c.nome_contratado or '—'}")
        lines.append(f"- **Objeto:** {objeto}")
        lines.append(f"- **Valor:** {valor}")
        lines.append("")

    if len(contratos) > 20:
        lines.append(f"*Mostrando 20 de {len(contratos)} contratos.*")
    return "\n".join(lines)
