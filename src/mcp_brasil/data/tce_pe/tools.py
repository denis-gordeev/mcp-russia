"""Tool functions for the TCE-PE feature.

Инструмент совместимости с API Счётного трибунала штата Пернамбуку (TCE-PE) Бразилии.
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


async def buscar_unidades_pe(
    ctx: Context,
    natureza: str = "prefeitura",
    municipio: str | None = None,
) -> str:
    """(legacy) Поиск подведомственных единиц TCE-PE (префектуры, палаты и т.д.).

    Примечание: инструмент совместимости для бразильских данных TCE-PE.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные системы SAGRES TCE-PE. Возвращает код и название
    единиц для использования в остальных запросах.

    Args:
        ctx: Контекст MCP.
        natureza: Тип единицы (напр.: "prefeitura", "câmara").
        municipio: Фильтр по муниципалитету (напр.: "Recife").

    Returns:
        Список единиц с кодом, названием и муниципалитетом.
    """
    await ctx.info(f"Buscando unidades do TCE-PE (natureza={natureza})...")
    unidades = await client.buscar_unidades(natureza=natureza, municipio=municipio)

    if not unidades:
        return "Nenhuma unidade jurisdicionada encontrada no TCE-PE."

    lines: list[str] = [f"**{len(unidades)} unidades no TCE-PE:**\n"]
    for u in unidades[:50]:
        lines.append(
            f"- **{u.nome or '—'}** (código: `{u.codigo}`, município: {u.municipio or '—'})"
        )

    if len(unidades) > 50:
        lines.append(f"\n*Mostrando 50 de {len(unidades)} unidades.*")
    return "\n".join(lines)


async def buscar_licitacoes_pe(
    ctx: Context,
    ano: int,
    municipio: str | None = None,
    modalidade: str | None = None,
) -> str:
    """(legacy) Поиск закупок Пернамбуку, зарегистрированных в TCE-PE.

    Примечание: инструмент совместимости для бразильских данных TCE-PE.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные системы LICON TCE-PE. Включает модальность, объект,
    оценочную стоимость и статус закупки.

    Args:
        ctx: Контекст MCP.
        ano: Год закупки (напр.: 2024).
        municipio: Фильтр по муниципалитету (напр.: "Recife").
        modalidade: Фильтр по модальности (напр.: "Pregão Eletrônico").

    Returns:
        Список закупок с объектом, модальностью и стоимостью.
    """
    await ctx.info(f"Buscando licitações no TCE-PE (ano={ano})...")
    licitacoes = await client.buscar_licitacoes(
        ano=ano, municipio=municipio, modalidade=modalidade
    )

    if not licitacoes:
        return "Nenhuma licitação encontrada no TCE-PE."

    lines: list[str] = [f"**{len(licitacoes)} licitações no TCE-PE:**\n"]
    for lic in licitacoes[:20]:
        valor = format_rub(lic.valor_estimado) if lic.valor_estimado else "—"
        objeto = (lic.objeto or "—")[:200]
        lines.append(f"### {lic.numero_licitacao or '—'}")
        lines.append(f"- **Município:** {lic.municipio or '—'}")
        lines.append(f"- **Modalidade:** {lic.modalidade or '—'}")
        lines.append(f"- **Objeto:** {objeto}")
        lines.append(f"- **Valor estimado:** {valor}")
        lines.append(f"- **Situação:** {lic.situacao or '—'}")
        lines.append("")

    if len(licitacoes) > 20:
        lines.append(f"*Mostrando 20 de {len(licitacoes)} licitações.*")
    return "\n".join(lines)


async def buscar_contratos_pe(
    ctx: Context,
    ano: int,
    municipio: str | None = None,
    cpf_cnpj: str | None = None,
) -> str:
    """(legacy) Поиск контрактов Пернамбуку, зарегистрированных в TCE-PE.

    Примечание: инструмент совместимости для бразильских данных TCE-PE.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные системы LICON TCE-PE. Включает объект, стоимость,
    поставщика и управляющую единицу.

    Args:
        ctx: Контекст MCP.
        ano: Год справки (напр.: 2024).
        municipio: Фильтр по муниципалитету (напр.: "Recife").
        cpf_cnpj: Фильтр по CPF/CNPJ поставщика.

    Returns:
        Список контрактов с объектом, стоимостью и поставщиком.
    """
    await ctx.info(f"Buscando contratos no TCE-PE (ano={ano})...")
    contratos = await client.buscar_contratos(ano=ano, municipio=municipio, cpf_cnpj=cpf_cnpj)

    if not contratos:
        return "Nenhum contrato encontrado no TCE-PE."

    lines: list[str] = [f"**{len(contratos)} contratos no TCE-PE:**\n"]
    for c in contratos[:20]:
        valor = format_rub(c.valor_contrato) if c.valor_contrato else "—"
        objeto = (c.objeto or "—")[:200]
        lines.append(f"### {c.numero_contrato or '—'}")
        lines.append(f"- **Município:** {c.municipio or '—'}")
        lines.append(f"- **Fornecedor:** {c.fornecedor or '—'}")
        lines.append(f"- **Objeto:** {objeto}")
        lines.append(f"- **Valor:** {valor}")
        lines.append("")

    if len(contratos) > 20:
        lines.append(f"*Mostrando 20 de {len(contratos)} contratos.*")
    return "\n".join(lines)


async def buscar_despesas_pe(
    ctx: Context,
    ano: int,
    mes: int | None = None,
    municipio: str | None = None,
    codigo_municipio: str | None = None,
) -> str:
    """(legacy) Поиск муниципальных расходов Пернамбуку, зарегистрированных в TCE-PE.

    Примечание: инструмент совместимости для бразильских данных TCE-PE.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные бюджетного исполнения системы SAGRES TCE-PE.
    Включает резервирования со значениями зарезервированных, ликвидированных и оплаченных.

    Args:
        ctx: Контекст MCP.
        ano: Год справки (напр.: 2024).
        mes: Месяц справки (1-12). Если пропущено, возвращает за весь год.
        municipio: Фильтр по названию муниципалитета.
        codigo_municipio: Код SAGRES муниципалитета.

    Returns:
        Список расходов с резервированием, поставщиком и стоимостью.
    """
    await ctx.info(f"Buscando despesas no TCE-PE (ano={ano})...")
    despesas = await client.buscar_despesas(
        ano=ano, mes=mes, municipio=municipio, codigo_municipio=codigo_municipio
    )

    if not despesas:
        return "Nenhuma despesa encontrada no TCE-PE."

    lines: list[str] = [f"**{len(despesas)} despesas no TCE-PE:**\n"]
    for d in despesas[:20]:
        empenhado = format_rub(d.valor_empenhado) if d.valor_empenhado else "—"
        pago = format_rub(d.valor_pago) if d.valor_pago else "—"
        historico = (d.historico or "—")[:150]
        lines.append(f"### Empenho {d.numero_empenho or '—'}")
        lines.append(f"- **Fornecedor:** {d.fornecedor or '—'}")
        lines.append(f"- **Empenhado:** {empenhado}")
        lines.append(f"- **Pago:** {pago}")
        lines.append(f"- **Função:** {d.funcao or '—'}")
        lines.append(f"- **Descrição:** {historico}")
        lines.append("")

    if len(despesas) > 20:
        lines.append(f"*Mostrando 20 de {len(despesas)} despesas.*")
    return "\n".join(lines)


async def buscar_fornecedores_pe(
    ctx: Context,
    nome: str | None = None,
    cpf_cnpj: str | None = None,
) -> str:
    """(legacy) Поиск поставщиков, зарегистрированных в TCE-PE.

    Примечание: инструмент совместимости для бразильских данных TCE-PE.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Данные системы SAGRES TCE-PE. Частичный поиск по названию или CPF/CNPJ.
    Рекомендуется хотя бы один фильтр во избежание избыточных результатов.

    Args:
        ctx: Контекст MCP.
        nome: Частичный поиск по названию поставщика.
        cpf_cnpj: Частичный поиск по CPF/CNPJ.

    Returns:
        Список поставщиков с названием и CPF/CNPJ.
    """
    await ctx.info("Buscando fornecedores no TCE-PE...")
    fornecedores = await client.buscar_fornecedores(nome=nome, cpf_cnpj=cpf_cnpj)

    if not fornecedores:
        return "Nenhum fornecedor encontrado no TCE-PE."

    lines: list[str] = [f"**{len(fornecedores)} fornecedores no TCE-PE:**\n"]
    for f in fornecedores[:30]:
        lines.append(f"- **{f.nome or '—'}** (CPF/CNPJ: `{f.cpf_cnpj or '—'}`)")

    if len(fornecedores) > 30:
        lines.append(f"\n*Mostrando 30 de {len(fornecedores)} fornecedores.*")
    return "\n".join(lines)
