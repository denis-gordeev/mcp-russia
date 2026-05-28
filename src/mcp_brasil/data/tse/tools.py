"""Инструменты для работы с TSE (Высший избирательный суд Бразилии, legacy).

Примечание: это слой совместимости в рамках mcp-russia. Данные инструменты
предоставляют устаревший доступ к данным бразильского Высшего избирательного
суда (Tribunal Superior Eleitoral) и считаются переходными.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_number_ru, format_rub, markdown_table

from . import client
from .constants import CARGO_CODES_CDN


async def anos_eleitorais() -> str:
    """(legacy) Список лет с доступными избирательными данными в TSE.

    Инструмент совместимости с TSE (Бразилия).
    Возвращает все годы, в которые проходили выборы с зарегистрированными данными.

    Returns:
        Список доступных избирательных лет.
    """
    anos = await client.anos_eleitorais()
    if not anos:
        return "Nenhum ano eleitoral disponível."
    return "Anos eleitorais disponíveis: " + ", ".join(str(a) for a in sorted(anos))


async def listar_eleicoes() -> str:
    """(legacy) Список всех очередных выборов, зарегистрированных в TSE.

    Инструмент совместимости с TSE (Бразилия).
    Включает муниципальные, региональные и федеральные выборы всех лет.

    Returns:
        Таблица с доступными выборами.
    """
    eleicoes = await client.listar_eleicoes()
    if not eleicoes:
        return "Nenhuma eleição encontrada."

    rows = [
        (
            str(e.id or "—"),
            str(e.ano or "—"),
            (e.nome or "—")[:40],
            e.tipo or "—",
            e.tipo_abrangencia or "—",
            e.data_eleicao or "—",
        )
        for e in eleicoes
    ]
    return f"Eleições ordinárias ({len(eleicoes)} registros):\n\n" + markdown_table(
        ["ID", "Ano", "Nome", "Tipo", "Abrangência", "Data"], rows
    )


async def listar_eleicoes_suplementares(ano: int, uf: str) -> str:
    """(legacy) Список дополнительных выборов штата за конкретный год.

    Инструмент совместимости с TSE (Бразилия).
    Дополнительные выборы проводятся при аннулировании обычных выборов
    или при вакантности выборной должности.

    Args:
        ano: Год выборов (напр.: 2020, 2022).
        uf: Аббревиатура штата (напр.: SP, RJ, MG).

    Returns:
        Таблица с найденными дополнительными выборами.
    """
    eleicoes = await client.listar_eleicoes_suplementares(ano, uf)
    if not eleicoes:
        return f"Nenhuma eleição suplementar encontrada para {uf.upper()} em {ano}."

    rows = [
        (
            str(e.id or "—"),
            str(e.ano or "—"),
            (e.nome or "—")[:40],
            e.tipo or "—",
            e.data_eleicao or "—",
        )
        for e in eleicoes
    ]
    return f"Eleições suplementares {uf.upper()} {ano} ({len(eleicoes)}):\n\n" + markdown_table(
        ["ID", "Ano", "Nome", "Tipo", "Data"], rows
    )


async def listar_estados_suplementares(ano: int) -> str:
    """(legacy) Список штатов с дополнительными выборами за год.

    Инструмент совместимости с TSE (Бразилия).
    Полезно для определения, какие штаты имели дополнительные выборы,
    перед запросом деталей через listar_eleicoes_suplementares().

    Args:
        ano: Год запроса (напр.: 2020, 2022).

    Returns:
        Список аббревиатур штатов с дополнительными выборами.
    """
    estados = await client.listar_estados_suplementares(ano)
    if not estados:
        return f"Nenhum estado com eleição suplementar em {ano}."
    return f"Estados com eleições suplementares em {ano}: {', '.join(sorted(estados))}"


async def listar_cargos(eleicao_id: int, municipio: int) -> str:
    """(legacy) Список доступных должностей в муниципалитете для выборов.

    Инструмент совместимости с TSE (Бразилия).
    Используйте ID выборов из listar_eleicoes() и код муниципалитета
    (код IBGE или TSE).

    Args:
        eleicao_id: ID выборов (напр.: 2030402020).
        municipio: Код муниципалитета (напр.: 35157 для Feira de Santana).

    Returns:
        Таблица с должностями и количеством кандидатов.
    """
    cargos = await client.listar_cargos(eleicao_id, municipio)
    if not cargos:
        return "Nenhum cargo encontrado para esta eleição/município."

    rows = [
        (
            str(c.codigo or "—"),
            c.nome or "—",
            "Sim" if c.titular else "Não",
            str(c.contagem or 0),
        )
        for c in cargos
    ]
    return f"Cargos disponíveis ({len(cargos)}):\n\n" + markdown_table(
        ["Código", "Cargo", "Titular", "Candidatos"], rows
    )


async def listar_candidatos(
    ano: int,
    municipio: int,
    eleicao_id: int,
    cargo: int,
) -> str:
    """(legacy) Список кандидатов на должность в муниципалитете.

    Инструмент совместимости с TSE (Бразилия).
    Требует ID выборов и должности из listar_eleicoes() и listar_cargos().

    Args:
        ano: Год выборов (напр.: 2020, 2022).
        municipio: Код муниципалитета.
        eleicao_id: ID выборов.
        cargo: Код должности (напр.: 11=Мэр, 13=Депутат).

    Returns:
        Таблица с кандидатами и их статусами.
    """
    candidatos = await client.listar_candidatos(ano, municipio, eleicao_id, cargo)
    if not candidatos:
        return "Nenhum candidato encontrado para os filtros informados."

    rows = [
        (
            str(c.id or "—"),
            (c.nome_urna or "—")[:30],
            str(c.numero or "—"),
            c.partido or "—",
            c.situacao or "—",
        )
        for c in candidatos
    ]
    return f"Candidatos ({len(candidatos)}):\n\n" + markdown_table(
        ["ID", "Nome de Urna", "Número", "Partido", "Situação"], rows
    )


async def buscar_candidato(
    ano: int,
    municipio: int,
    eleicao_id: int,
    candidato_id: int,
) -> str:
    """(legacy) Поиск полной информации о кандидате.

    Инструмент совместимости с TSE (Бразилия).
    Возвращает личные данные, избирательную информацию, декларированное
    имущество и статус кандидатуры.

    Args:
        ano: Год выборов.
        municipio: Код муниципалитета.
        eleicao_id: ID выборов.
        candidato_id: ID кандидата (из listar_candidatos).

    Returns:
        Полная карточка кандидата.
    """
    cand = await client.buscar_candidato(ano, municipio, eleicao_id, candidato_id)
    if cand is None:
        return "Candidato não encontrado."

    lines = [
        f"**Nome de urna:** {cand.nome_urna or '—'}",
        f"**Nome completo:** {cand.nome_completo or '—'}",
        f"**Número:** {cand.numero or '—'}",
        f"**Partido:** {cand.partido or '—'}",
        f"**Coligação:** {cand.coligacao or '—'}",
        f"**Situação:** {cand.situacao or '—'}",
        f"**Situação do candidato:** {cand.situacao_candidato or '—'}",
    ]

    if cand.descricao_totalizacao:
        lines.append(f"**Resultado:** {cand.descricao_totalizacao}")
    if cand.total_votos is not None:
        lines.append(f"**Total de votos:** {format_number_ru(cand.total_votos, 0)}")

    lines.append("\n**Dados pessoais:**")
    lines.append(f"  Sexo: {cand.sexo or '—'}")
    lines.append(f"  Cor/Raça: {cand.cor_raca or '—'}")
    lines.append(f"  Estado civil: {cand.estado_civil or '—'}")
    lines.append(f"  Escolaridade: {cand.grau_instrucao or '—'}")
    lines.append(f"  Ocupação: {cand.ocupacao or '—'}")
    lines.append(f"  Naturalidade: {cand.municipio_nascimento or '—'}/{cand.uf_nascimento or '—'}")

    if cand.total_bens is not None:
        lines.append(f"\n**Total de bens declarados:** {format_rub(cand.total_bens)}")

    if cand.gasto_campanha is not None and cand.gasto_campanha > 0:
        lines.append(f"**Gasto de campanha:** {format_rub(cand.gasto_campanha)}")

    if cand.candidato_inapto:
        lines.append("\n**CANDIDATO INAPTO**")
    if cand.motivo_ficha_limpa:
        lines.append("**Motivo Ficha Limpa aplicado**")

    return "\n".join(lines)


async def resultado_eleicao(
    ano: int,
    municipio: int,
    eleicao_id: int,
    cargo: int,
) -> str:
    """(legacy) Результат выборов с кандидатами, ранжированными по голосам.

    Инструмент совместимости с TSE (Бразилия).
    Возвращает итоговый подсчёт голосов всех кандидатов по должности
    в муниципалитете, отсортированный от большинства к меньшинству.

    Args:
        ano: Год выборов (напр.: 2020, 2022).
        municipio: Код муниципалитета.
        eleicao_id: ID выборов.
        cargo: Код должности (напр.: 11=Мэр, 13=Депутат).

    Returns:
        Таблица с рейтингом кандидатов по голосам.
    """
    resultados = await client.resultado_eleicao(ano, municipio, eleicao_id, cargo)
    if not resultados:
        return "Nenhum resultado encontrado para os filtros informados."

    rows = [
        (
            str(i),
            (r.nome_urna or "—")[:30],
            str(r.numero or "—"),
            r.partido or "—",
            format_number_ru(r.total_votos, 0) if r.total_votos is not None else "—",
            r.percentual or "—",
            (r.descricao_totalizacao or "—")[:20],
        )
        for i, r in enumerate(resultados, 1)
    ]
    return f"Resultado da eleição ({len(resultados)} candidatos):\n\n" + markdown_table(
        ["#", "Nome", "Nº", "Partido", "Votos", "%", "Resultado"], rows
    )


async def consultar_prestacao_contas(
    eleicao_id: int,
    ano: int,
    municipio: int,
    cargo: int,
    candidato_id: int,
) -> str:
    """(legacy) Запрос финансовой отчётности кампании кандидата.

    Инструмент совместимости с TSE (Бразилия).
    Возвращает доходы, расходы, доноров, поставщиков и лимиты расходов.

    Args:
        eleicao_id: ID выборов.
        ano: Год выборов.
        municipio: Код муниципалитета.
        cargo: Код должности.
        candidato_id: ID кандидата.

    Returns:
        Финансовое резюме кампании.
    """
    contas = await client.consultar_prestacao_contas(
        eleicao_id, ano, municipio, cargo, candidato_id
    )
    if contas is None:
        return "Prestação de contas não encontrada para este candidato."

    lines = [
        f"**Candidato:** {contas.nome or '—'}",
        f"**Partido:** {contas.partido or '—'}",
        f"**CNPJ campanha:** {contas.cnpj or '—'}",
    ]

    lines.append("\n**Receitas:**")
    lines.append(f"  Total recebido: {format_rub(contas.total_recebido or 0)}")
    lines.append(f"  Pessoa física: {format_rub(contas.total_receita_pf or 0)}")
    lines.append(f"  Pessoa jurídica: {format_rub(contas.total_receita_pj or 0)}")
    lines.append(f"  Fundo partidário: {format_rub(contas.total_fundo_partidario or 0)}")
    lines.append(f"  Fundo especial: {format_rub(contas.total_fundo_especial or 0)}")

    lines.append("\n**Despesas:**")
    lines.append(f"  Total despesas: {format_rub(contas.total_despesas or 0)}")
    lines.append(f"  Limite de gastos: {format_rub(contas.limite_gastos or 0)}")

    if contas.divida_campanha:
        lines.append(f"\n**Dívida de campanha:** {contas.divida_campanha}")
    if contas.sobra_financeira:
        lines.append(f"**Sobra financeira:** {contas.sobra_financeira}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CDN de Resultados — votação por região (país, estado, município)
# ---------------------------------------------------------------------------


def _cargos_disponiveis() -> str:
    """Возвращает список доступных наименований должностей через запятую."""
    return ", ".join(CARGO_CODES_CDN.keys())


async def resultado_nacional(
    ano: int,
    cargo: str,
    ctx: Context,
    turno: int = 1,
) -> str:
    """(legacy) Национальный результат выборов со всеми кандидатами.

    Инструмент совместимости с TSE (Бразилия).
    Возвращает итоговый подсчёт на национальном уровне: избиратели,
    явка, прогулы и рейтинг кандидатов по голосам.

    Доступные должности: presidente, governador, senador, deputado_federal,
    deputado_estadual, prefeito, vereador.

    Доступные выборы: 2022 (федеральные) и 2024 (муниципальные).

    Args:
        ano: Год выборов (напр.: 2022, 2024).
        cargo: Название должности (напр.: "presidente", "prefeito").
        turno: Тур выборов (1 или 2). По умолчанию: 1.

    Returns:
        Таблица с национальным рейтингом кандидатов по голосам.
    """
    await ctx.info(f"Buscando resultado nacional {cargo} {ano} T{turno}...")

    try:
        resultado = await client.resultado_simplificado(ano, cargo, "br", turno)
    except ValueError as e:
        return str(e)

    if resultado is None or not resultado.candidatos:
        return f"Resultado não encontrado para {cargo} {ano} turno {turno}."

    header_lines = [
        f"**Resultado Nacional — {cargo.replace('_', ' ').title()} {ano} (T{turno})**\n",
        f"Apuração: {resultado.pct_apurado}% das seções",
    ]
    if resultado.total_eleitores:
        header_lines.append(f"Eleitores: {format_number_ru(resultado.total_eleitores, 0)}")
    if resultado.total_comparecimento:
        header_lines.append(
            f"Comparecimento: {format_number_ru(resultado.total_comparecimento, 0)}"
        )
    if resultado.total_abstencoes:
        header_lines.append(f"Abstenções: {format_number_ru(resultado.total_abstencoes, 0)}")

    rows = [
        (
            str(i),
            (c.nome or "—")[:25],
            c.numero or "—",
            format_number_ru(c.votos, 0) if c.votos else "—",
            f"{c.percentual}%" if c.percentual else "—",
            (c.situacao or "—")[:15],
        )
        for i, c in enumerate(resultado.candidatos, 1)
    ]

    return (
        "\n".join(header_lines)
        + "\n\n"
        + markdown_table(["#", "Candidato", "Nº", "Votos", "%", "Situação"], rows)
    )


async def resultado_por_estado(
    ano: int,
    cargo: str,
    uf: str,
    ctx: Context,
    turno: int = 1,
) -> str:
    """(legacy) Результат выборов в конкретном штате.

    Инструмент совместимости с TSE (Бразилия).
    Возвращает подсчёт голосов каждого кандидата в этом штате.

    Args:
        ano: Год выборов (напр.: 2022, 2024).
        cargo: Название должности (напр.: "presidente", "governador").
        uf: Аббревиатура штата (напр.: "SP", "RJ", "PI").
        turno: Тур выборов (1 или 2). По умолчанию: 1.

    Returns:
        Таблица с рейтингом кандидатов в штате.
    """
    await ctx.info(f"Buscando resultado {cargo} {ano} em {uf.upper()}...")

    try:
        resultado = await client.resultado_simplificado(ano, cargo, uf, turno)
    except ValueError as e:
        return str(e)

    if resultado is None or not resultado.candidatos:
        return f"Resultado não encontrado para {cargo} {ano} T{turno} em {uf.upper()}."

    header_lines = [
        f"**Resultado {uf.upper()} — {cargo.replace('_', ' ').title()} {ano} (T{turno})**\n",
        f"Apuração: {resultado.pct_apurado}% das seções",
    ]
    if resultado.total_eleitores:
        header_lines.append(f"Eleitores: {format_number_ru(resultado.total_eleitores, 0)}")

    rows = [
        (
            str(i),
            (c.nome or "—")[:25],
            c.numero or "—",
            format_number_ru(c.votos, 0) if c.votos else "—",
            f"{c.percentual}%" if c.percentual else "—",
        )
        for i, c in enumerate(resultado.candidatos, 1)
    ]

    return (
        "\n".join(header_lines)
        + "\n\n"
        + markdown_table(["#", "Candidato", "Nº", "Votos", "%"], rows)
    )


async def mapa_resultado_estados(
    ano: int,
    cargo: str,
    ctx: Context,
    turno: int = 1,
) -> str:
    """(legacy) Победители в каждом штате — полная карта выборов.

    Инструмент совместимости с TSE (Бразилия).
    Параллельный запрос по всем 27 штатам, возвращает кандидата
    с наибольшим числом голосов в каждом штате.

    Args:
        ano: Год выборов (напр.: 2022).
        cargo: Название должности (напр.: "presidente").
        turno: Тур выборов (1 или 2). По умолчанию: 1.

    Returns:
        Таблица с победителями каждого штата.
    """
    await ctx.info(f"Buscando mapa eleitoral {cargo} {ano} T{turno} (27 UFs)...")

    try:
        resultados = await client.resultado_todos_estados(ano, cargo, turno)
    except ValueError as e:
        return str(e)

    if not resultados:
        return f"Nenhum resultado encontrado para {cargo} {ano} turno {turno}."

    rows = []
    for r in sorted(resultados, key=lambda x: (x.uf or "").upper()):
        if not r.candidatos:
            continue
        vencedor = r.candidatos[0]
        rows.append(
            (
                (r.uf or "—").upper(),
                (vencedor.nome or "—")[:20],
                vencedor.numero or "—",
                format_number_ru(vencedor.votos, 0) if vencedor.votos else "—",
                f"{vencedor.percentual}%" if vencedor.percentual else "—",
                f"{r.pct_apurado}%" if r.pct_apurado else "—",
            )
        )

    header = (
        f"**Mapa Eleitoral — {cargo.replace('_', ' ').title()} {ano} (T{turno})**\n"
        f"{len(rows)} estados com dados\n"
    )
    return (
        header + "\n" + markdown_table(["UF", "Mais votado", "Nº", "Votos", "%", "Apuração"], rows)
    )


async def listar_municipios_eleitorais(
    ano: int,
    uf: str,
    ctx: Context,
    turno: int = 1,
) -> str:
    """(legacy) Список избирательных муниципалитетов штата с кодами TSE и IBGE.

    Инструмент совместимости с TSE (Бразилия).
    Возвращает муниципалитеты, доступные для запроса результатов.
    Доступно только для муниципальных выборов (2024).

    Используйте codigo_tse как параметр для resultado_por_municipio().

    Args:
        ano: Год выборов (напр.: 2024).
        uf: Аббревиатура штата (напр.: "SP", "RJ").
        turno: Тур выборов (1 или 2). По умолчанию: 1.

    Returns:
        Таблица с муниципалитетами и их кодами TSE/IBGE.
    """
    await ctx.info(f"Buscando municípios eleitorais de {uf.upper()} {ano}...")

    try:
        municipios = await client.listar_municipios_eleitorais(ano, uf, turno)
    except ValueError as e:
        return str(e)

    if not municipios:
        return f"Nenhum município encontrado para {uf.upper()} {ano} turno {turno}."

    rows = [
        (
            m.codigo_tse or "—",
            m.codigo_ibge or "—",
            (m.nome or "—")[:30],
            "Sim" if m.capital else "Não",
        )
        for m in municipios
    ]
    return f"Municípios eleitorais {uf.upper()} {ano} ({len(municipios)}):\n\n" + markdown_table(
        ["Cód. TSE", "Cód. IBGE", "Nome", "Capital"], rows
    )


async def resultado_por_municipio(
    ano: int,
    cargo: str,
    uf: str,
    cod_tse: str,
    ctx: Context,
    turno: int = 1,
) -> str:
    """(legacy) Результат выборов в конкретном муниципалитете.

    Инструмент совместимости с TSE (Бразилия).
    Возвращает подсчёт голосов каждого кандидата в муниципалитете.
    Доступно для федеральных (2022) и муниципальных (2024) выборов.

    Используйте listar_municipios_eleitorais() для получения кода TSE.

    Должности 2022: presidente, governador, senador, deputado_federal, deputado_estadual.
    Должности 2024: prefeito, vereador.

    Args:
        ano: Год выборов (напр.: 2022, 2024).
        cargo: Название должности (напр.: "presidente", "governador", "prefeito").
        uf: Аббревиатура штата (напр.: "SP", "RJ").
        cod_tse: Код TSE муниципалитета (5 цифр, напр.: "71072" для Сан-Паулу).
        turno: Тур выборов (1 или 2). По умолчанию: 1.

    Returns:
        Таблица с рейтингом кандидатов по голосам в муниципалитете.
    """
    await ctx.info(f"Buscando resultado {cargo} {ano} em {uf.upper()} (município {cod_tse})...")

    try:
        resultado = await client.resultado_municipio(ano, cargo, uf, cod_tse, turno)
    except ValueError as e:
        return str(e)

    if resultado is None or not resultado.candidatos:
        return (
            f"Resultado não encontrado para {cargo} {ano} T{turno} "
            f"em {uf.upper()} município {cod_tse}."
        )

    header_lines = [
        f"**Resultado Município {cod_tse} ({uf.upper()}) — "
        f"{cargo.replace('_', ' ').title()} {ano} (T{turno})**\n",
        f"Apuração: {resultado.pct_apurado}% das seções",
    ]
    if resultado.total_eleitores:
        header_lines.append(f"Eleitores: {format_number_ru(resultado.total_eleitores, 0)}")

    rows = [
        (
            str(i),
            (c.nome or "—")[:25],
            c.numero or "—",
            format_number_ru(c.votos, 0) if c.votos else "—",
            f"{c.percentual}%" if c.percentual else "—",
        )
        for i, c in enumerate(resultado.candidatos, 1)
    ]

    return (
        "\n".join(header_lines)
        + "\n\n"
        + markdown_table(["#", "Candidato", "Nº", "Votos", "%"], rows)
    )


async def apuracao_status(
    ano: int,
    cargo: str,
    ctx: Context,
    uf: str = "br",
    turno: int = 1,
) -> str:
    """(legacy) Статус подсчёта голосов на выборах.

    Инструмент совместимости с TSE (Бразилия).
    Возвращает процент подсчитанных участков, общее число избирателей,
    явку и прогулы.

    Args:
        ano: Год выборов.
        cargo: Название должности.
        uf: Аббревиатура штата или "br" для национального. По умолчанию: "br".
        turno: Тур выборов. По умолчанию: 1.

    Returns:
        Сводка статуса подсчёта.
    """
    regiao_label = "Nacional" if uf.lower() == "br" else uf.upper()
    await ctx.info(f"Consultando apuração {cargo} {ano} ({regiao_label})...")

    try:
        resultado = await client.resultado_simplificado(ano, cargo, uf, turno)
    except ValueError as e:
        return str(e)

    if resultado is None:
        return f"Dados de apuração não encontrados para {cargo} {ano} T{turno}."

    lines = [
        f"**Status da Apuração — {cargo.replace('_', ' ').title()} {ano} (T{turno})**",
        f"**Região:** {regiao_label}",
        f"**Seções apuradas:** {resultado.pct_apurado}%"
        + (f" de {format_number_ru(resultado.total_secoes, 0)}" if resultado.total_secoes else ""),
    ]

    if resultado.total_eleitores:
        lines.append(f"**Eleitores:** {format_number_ru(resultado.total_eleitores, 0)}")
    if resultado.total_comparecimento:
        lines.append(f"**Comparecimento:** {format_number_ru(resultado.total_comparecimento, 0)}")
    if resultado.total_abstencoes and resultado.total_eleitores:
        pct_abs = resultado.total_abstencoes / resultado.total_eleitores * 100
        lines.append(
            f"**Abstenções:** {format_number_ru(resultado.total_abstencoes, 0)} ({pct_abs:.1f}%)"
        )

    return "\n".join(lines)
