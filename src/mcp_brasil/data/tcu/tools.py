"""Инструменты для работы с TCU (Счётная палата Бразилии, legacy).

Примечание: это слой совместимости в рамках mcp-russia. Данные инструменты
предоставляют устаревший доступ к данным бразильской Счётной палаты
(Tribunal de Contas da União) и считаются переходными.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
    - Использует Context для структурированного логирования и отчёта о прогрессе
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_rub

from . import client
from .schemas import ParcelaDebito

# ---------------------------------------------------------------------------
# buscar_acordaos
# ---------------------------------------------------------------------------


async def buscar_acordaos(
    ctx: Context,
    inicio: int = 0,
    quantidade: int = 20,
) -> str:
    """(legacy) Поиск постановлений (коллегиальных решений) TCU.

    Инструмент совместимости с TCU (Бразилия).
    Acórdãos — формальные решения Счётной палаты, включая рассмотрение
    отчётов, аудиты и апелляции. Возвращает недавние решения.

    Args:
        ctx: Контекст MCP.
        inicio: Начальный индекс для пагинации (0 = самые свежие).
        quantidade: Количество постановлений (макс. ~50).

    Returns:
        Форматированный список постановлений с заголовком и кратким содержанием.
    """
    await ctx.info(f"Buscando acórdãos do TCU (início={inicio})...")
    acordaos = await client.buscar_acordaos(inicio=inicio, quantidade=quantidade)

    if not acordaos:
        return "Nenhum acórdão encontrado."

    lines: list[str] = [f"**{len(acordaos)} acórdãos do TCU:**\n"]
    for a in acordaos[:20]:
        lines.append(f"### {a.titulo or 'Sem título'}")
        lines.append(f"- **Colegiado:** {a.colegiado or '—'}")
        lines.append(f"- **Relator:** {a.relator or '—'}")
        lines.append(f"- **Data sessão:** {a.data_sessao or '—'}")
        lines.append(f"- **Situação:** {a.situacao or '—'}")
        if a.sumario:
            sumario = a.sumario[:300] + "..." if len(a.sumario) > 300 else a.sumario
            lines.append(f"- **Sumário:** {sumario}")
        if a.url_acordao:
            lines.append(f"- **Link:** {a.url_acordao}")
        lines.append("")

    if len(acordaos) >= quantidade:
        lines.append(
            f"\n*Página com {quantidade} resultados. "
            f"Use inicio={inicio + quantidade} para próxima página.*"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# consultar_inabilitados
# ---------------------------------------------------------------------------


async def consultar_inabilitados(
    ctx: Context,
    cpf: str | None = None,
    offset: int = 0,
    limit: int = 25,
) -> str:
    """(legacy) Запрос лиц, лишённых права занимать государственные должности по решению TCU.

    Инструмент совместимости с TCU (Бразилия).
    Лишённые права не могут занимать должности в комиссии или функции
    доверия в Федеральной публичной администрации. Поиск по CPF или полный список.

    Args:
        ctx: Контекст MCP.
        cpf: CPF для конкретного запроса (только цифры).
        offset: Смещение для пагинации.
        limit: Количество на страницу (по умолчанию 25).

    Returns:
        Список лишённых права лиц с данными о санкции.
    """
    await ctx.info("Consultando inabilitados no TCU...")
    resultado = await client.consultar_inabilitados(cpf=cpf, offset=offset, limit=limit)

    if not resultado.items:
        if cpf:
            return f"CPF {cpf} **não consta** na lista de inabilitados do TCU."
        return "Nenhum inabilitado encontrado."

    lines: list[str] = [f"**{resultado.count} inabilitado(s) encontrado(s):**\n"]
    for item in resultado.items:
        lines.append(f"### {item.nome or '—'}")
        lines.append(f"- **CPF:** {item.cpf or '—'}")
        lines.append(f"- **Processo:** {item.processo or '—'}")
        lines.append(f"- **Deliberação:** {item.deliberacao or '—'}")
        lines.append(f"- **UF:** {item.uf or '—'}")
        if item.data_final:
            lines.append(f"- **Inabilitado até:** {item.data_final}")
        lines.append("")

    if resultado.has_more:
        next_offset = resultado.offset + resultado.limit
        lines.append(
            f"*Mais resultados disponíveis. Use offset={next_offset} para próxima página.*"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# consultar_inidoneos
# ---------------------------------------------------------------------------


async def consultar_inidoneos(
    ctx: Context,
    cpf_cnpj: str | None = None,
    offset: int = 0,
    limit: int = 25,
) -> str:
    """(legacy) Запрос компаний/лиц, объявленных недобросовестными TCU.

    Инструмент совместимости с TCU (Бразилия).
    Объявленные недобросовестными не могут участвовать в тендерах
    Федеральной публичной администрации. Поиск по CPF/CNPJ или полный список.

    Args:
        ctx: Контекст MCP.
        cpf_cnpj: CPF или CNPJ для конкретного запроса (только цифры).
        offset: Смещение для пагинации.
        limit: Количество на страницу (по умолчанию 25).

    Returns:
        Список недобросовестных участников с данными о санкции.
    """
    await ctx.info("Consultando inidôneos no TCU...")
    resultado = await client.consultar_inidoneos(cpf_cnpj=cpf_cnpj, offset=offset, limit=limit)

    if not resultado.items:
        if cpf_cnpj:
            return f"CPF/CNPJ {cpf_cnpj} **não consta** na lista de inidôneos do TCU."
        return "Nenhum inidôneo encontrado."

    lines: list[str] = [f"**{resultado.count} inidôneo(s) encontrado(s):**\n"]
    for item in resultado.items:
        lines.append(f"### {item.nome or '—'}")
        lines.append(f"- **CPF/CNPJ:** {item.cpf_cnpj or '—'}")
        lines.append(f"- **Processo:** {item.processo or '—'}")
        lines.append(f"- **Deliberação:** {item.deliberacao or '—'}")
        lines.append(f"- **UF:** {item.uf or '—'}")
        if item.data_final:
            lines.append(f"- **Inidôneo até:** {item.data_final}")
        lines.append("")

    if resultado.has_more:
        next_offset = resultado.offset + resultado.limit
        lines.append(
            f"*Mais resultados disponíveis. Use offset={next_offset} para próxima página.*"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# consultar_certidoes_apf
# ---------------------------------------------------------------------------


async def consultar_certidoes_apf(cnpj: str, ctx: Context) -> str:
    """(legacy) Запрос консолидированных сертификатов юридического лица (APF).

    Инструмент совместимости с TCU (Бразилия).
    Проверяет компанию в 4 реестрах одновременно:
    - **TCU Inidôneos**: недобросовестные участники торгов
    - **CNJ CNIA**: осуждения за административное правонарушение
    - **CGU CEIS**: недобросовестные и приостановленные компании
    - **CGU CNEP**: наказанные компании

    Полезно для проверки добросовестности (due diligence) поставщиков.

    Args:
        cnpj: CNPJ компании (только цифры, 14 знаков).
        ctx: Контекст MCP.

    Returns:
        Консолидированный статус компании в 4 реестрах.
    """
    await ctx.info(f"Consultando certidões APF para CNPJ {cnpj}...")
    resultado = await client.consultar_certidoes(cnpj)

    lines: list[str] = []
    lines.append(f"## Certidões APF — {resultado.razao_social or cnpj}")
    if resultado.nome_fantasia:
        lines.append(f"**Nome fantasia:** {resultado.nome_fantasia}")
    lines.append(f"**CNPJ:** {resultado.cnpj or cnpj}")
    lines.append("")

    if not resultado.certidoes:
        lines.append("Nenhuma certidão retornada.")
        return "\n".join(lines)

    for cert in resultado.certidoes:
        situacao = cert.situacao or "—"
        emoji = "NADA_CONSTA" if situacao == "NADA_CONSTA" else "CONSTA"
        status_label = "Nada consta" if emoji == "NADA_CONSTA" else situacao
        lines.append(f"- **{cert.emissor} ({cert.tipo}):** {status_label}")
        if cert.observacao:
            lines.append(f"  - Obs: {cert.observacao}")

    lines.append("")
    if not resultado.cnpj_encontrado_base_tcu:
        lines.append("*CNPJ não encontrado na base do TCU.*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# calcular_debito_tcu
# ---------------------------------------------------------------------------


async def calcular_debito_tcu(
    data_atualizacao: str,
    data_fato: str,
    valor_original: float,
    ctx: Context,
    aplica_juros: bool = True,
    tipo: str = "D",
) -> str:
    """(legacy) Расчёт обновлённой задолженности с денежной коррекцией (вариация SELIC).

    Инструмент совместимости с TCU (Бразилия).
    Использует официальный калькулятор TCU для обновления сумм задолженности.
    Применяет денежную коррекцию по вариации ставки SELIC и, опционально, проценты.

    Args:
        data_atualizacao: Дата обновления в формате DD/MM/YYYY.
        data_fato: Дата факта в формате DD/MM/YYYY.
        valor_original: Сумма задолженности в реалах.
        ctx: Контекст MCP.
        aplica_juros: Применять ли проценты (по умолчанию: True).
        tipo: "D" для задолженности, "C" для кредита (по умолчанию: "D").

    Returns:
        Детализация расчёта с обновлённой суммой.
    """
    await ctx.info("Calculando débito atualizado no TCU...")
    parcela = ParcelaDebito(
        data_fato=data_fato,
        indicativo_debito_credito=tipo,
        valor_original=valor_original,
    )
    resultado = await client.calcular_debito(
        data_atualizacao=data_atualizacao,
        aplica_juros=aplica_juros,
        parcelas=[parcela],
    )

    lines = [
        "## Cálculo de Débito — TCU\n",
        f"- **Data do fato:** {data_fato}",
        f"- **Data de atualização:** {resultado.data or data_atualizacao}",
        f"- **Valor original:** {format_rub(valor_original)}",
        f"- **Correção monetária (SELIC):** {format_rub(resultado.saldo_variacao_selic)}",
        f"- **Juros de mora:** {format_rub(resultado.saldo_juros)}",
        f"- **Valor total atualizado:** {format_rub(resultado.saldo_total)}",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# buscar_pedidos_congresso
# ---------------------------------------------------------------------------


async def buscar_pedidos_congresso(
    ctx: Context,
    processo: str | None = None,
    page: int | None = None,
) -> str:
    """(legacy) Поиск запросов Национального конгресса в TCU.

    Инструмент совместимости с TCU (Бразилия).
    Запросы и требования парламентариев к Счётной палате.
    Поиск по номеру процесса или полный список.

    Args:
        ctx: Контекст MCP.
        processo: Номер процесса TCU для фильтрации (напр.: "004.808/2026-6").
        page: Страница результатов.

    Returns:
        Список запросов с автором, темой и ссылками.
    """
    await ctx.info("Buscando pedidos do Congresso ao TCU...")
    resultado = await client.buscar_pedidos_congresso(processo=processo, page=page)

    if not resultado.items:
        return "Nenhum pedido do Congresso encontrado."

    lines: list[str] = [f"**{len(resultado.items)} pedido(s) do Congresso:**\n"]
    for item in resultado.items[:20]:
        lines.append(f"### {item.tipo or '—'} nº {item.numero or '—'}")
        lines.append(f"- **Autor:** {item.autor or '—'}")
        lines.append(f"- **Processo:** {item.processo_scn or '—'}")
        if item.data_aprovacao:
            lines.append(f"- **Data aprovação:** {item.data_aprovacao}")
        if item.assunto:
            assunto = item.assunto[:300] + "..." if len(item.assunto) > 300 else item.assunto
            lines.append(f"- **Assunto:** {assunto}")
        lines.append("")

    if resultado.has_next:
        next_page = (page or 0) + 1
        lines.append(f"*Mais resultados. Use page={next_page} para próxima página.*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# buscar_contratos_tcu
# ---------------------------------------------------------------------------


async def buscar_contratos_tcu(ctx: Context) -> str:
    """(legacy) Поиск контрактов, заключённых самим TCU.

    Инструмент совместимости с TCU (Бразилия).
    Возвращает полный список контрактов Счётной палаты, включая
    закупки, аукционы и прямые контракты. Полезно для прозрачности
    расходов самого контролирующего органа.

    Args:
        ctx: Контекст MCP.

    Returns:
        Краткий список самых недавних контрактов TCU.
    """
    await ctx.info("Buscando contratos do TCU...")
    contratos = await client.buscar_contratos_tcu()

    if not contratos:
        return "Nenhum contrato do TCU encontrado."

    contratos.sort(key=lambda c: (c.ano or 0, c.numero or 0), reverse=True)
    amostra = contratos[:20]

    lines: list[str] = [
        f"**{len(contratos)} contratos do TCU** (mostrando {len(amostra)} mais recentes):\n"
    ]
    for c in amostra:
        valor = format_rub(c.valor_atualizado) if c.valor_atualizado else "—"
        lines.append(f"### {c.numero or '—'}/{c.ano or '—'}")
        lines.append(f"- **Fornecedor:** {c.nome_fornecedor or '—'}")
        lines.append(f"- **Objeto:** {c.objeto or '—'}")
        lines.append(f"- **Valor atualizado:** {valor}")
        lines.append(f"- **Modalidade:** {c.modalidade_licitacao or '—'}")
        lines.append(f"- **Processo:** {c.numero_processo or '—'}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# consultar_cadirreg
# ---------------------------------------------------------------------------


async def consultar_cadirreg(cpf: str, ctx: Context) -> str:
    """(legacy) Запрос лица в CADIRREG — реестре лиц с нерегулярными отчётами.

    Инструмент совместимости с TCU (Бразилия).
    Проверяет, имеет ли CPF счета с нерегулярными отчётами, рассмотренными TCU.
    Лица в этом реестре имели свои счета отклонённые в процессах внешнего контроля.

    Args:
        cpf: CPF лица (только цифры, 11 знаков).
        ctx: Контекст MCP.

    Returns:
        Данные о нерегулярных счетах или подтверждение отсутствия записей.
    """
    await ctx.info(f"Consultando CADIRREG para CPF {cpf}...")
    registros = await client.consultar_cadirreg(cpf)

    if not registros:
        return f"CPF {cpf} **não consta** no CADIRREG do TCU."

    lines: list[str] = [f"**{len(registros)} registro(s) no CADIRREG para CPF {cpf}:**\n"]
    for r in registros:
        lines.append(f"### {r.nome_responsavel or '—'}")
        lines.append(f"- **Processo:** {r.num_processo or '—'}/{r.ano_processo or '—'}")
        lines.append(f"- **Julgamento:** {r.julgamento or '—'}")
        lines.append(f"- **Unidade técnica:** {r.unidade_tecnica_processo or '—'}")
        if r.se_detentor_cargo_funcao_publica:
            lines.append(f"- **Detentor de cargo público:** {r.se_detentor_cargo_funcao_publica}")
        lines.append("")

    return "\n".join(lines)
