"""Инструменты для работы с Порталом прозрачности Бразилии (слой совместимости, legacy).

Примечание: это слой совместимости в рамках mcp-russia. Данные инструменты
предоставляют устаревший доступ к данным бразильского Портала прозрачности
(Portal da Transparência) и считаются переходными.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from mcp_russia._shared.formatting import format_rub, markdown_table, truncate_list
from mcp_russia.exceptions import HttpClientError

from . import client
from .constants import DEFAULT_PAGE_SIZE


def _pagination_hint(count: int, pagina: int) -> str:
    """Возвращает подсказку о пагинации на основе количества результатов и текущей страницы."""
    if count >= DEFAULT_PAGE_SIZE:
        return f"\n\n> Use `pagina={pagina + 1}` para ver mais resultados."
    if pagina > 1 and count < DEFAULT_PAGE_SIZE:
        return "\n\n> Última página de resultados."
    return ""


async def buscar_contratos(cpf_cnpj: str, pagina: int = 1) -> str:
    """(legacy) Поиск федеральных контрактов по CPF или CNPJ поставщика.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Запрос контрактов, заключённых с федеральным правительством.

    Args:
        cpf_cnpj: CPF или CNPJ поставщика (с форматированием или без).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными контрактами.
    """
    contratos = await client.buscar_contratos(cpf_cnpj, pagina)
    if not contratos:
        return f"Nenhum contrato encontrado para o CPF/CNPJ '{cpf_cnpj}'."

    rows = [
        (
            c.numero or "—",
            (c.objeto or "—")[:80],
            format_rub(c.valor_final) if c.valor_final else "—",
            c.data_inicio or "—",
            c.data_fim or "—",
            (c.orgao or "—")[:40],
        )
        for c in contratos
    ]
    header = f"Contratos do fornecedor {cpf_cnpj} (página {pagina}):\n\n"
    table = header + markdown_table(
        ["Número", "Objeto", "Valor Final", "Início", "Fim", "Órgão"], rows
    )
    return table + _pagination_hint(len(contratos), pagina)


async def consultar_despesas(
    mes_ano_inicio: str,
    mes_ano_fim: str,
    codigo_favorecido: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Запрос расходов и поступлений получателя бюджетных средств.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Показывает выплаты, произведённые федеральным правительством.

    Args:
        mes_ano_inicio: Месяц/год начала в формате MM/YYYY (напр.: 01/2024).
        mes_ano_fim: Месяц/год окончания в формате MM/YYYY (напр.: 12/2024).
        codigo_favorecido: CPF или CNPJ получателя (необязательно).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными расходами.
    """
    despesas = await client.consultar_despesas(
        mes_ano_inicio, mes_ano_fim, codigo_favorecido, pagina
    )
    if not despesas:
        return "Nenhuma despesa encontrada para os parâmetros informados."

    rows = [
        (
            f"{d.mes or '—'}/{d.ano or '—'}",
            (d.favorecido_nome or "—")[:50],
            format_rub(d.valor) if d.valor else "—",
            (d.orgao_nome or "—")[:40],
            d.uf or "—",
        )
        for d in despesas
    ]
    header = f"Despesas de {mes_ano_inicio} a {mes_ano_fim} (página {pagina}):\n\n"
    table = header + markdown_table(["Período", "Favorecido", "Valor", "Órgão", "UF"], rows)
    return table + _pagination_hint(len(despesas), pagina)


async def buscar_servidores(
    cpf: str | None = None,
    nome: str | None = None,
    codigo_orgao_lotacao: str | None = None,
    codigo_orgao_exercicio: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск федеральных государственных служащих по CPF, имени или органу.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    API требует хотя бы одного: CPF, код органа назначения или код органа
    фактической работы. Одно только имя не принимается — комбинируйте с кодом органа.

    Args:
        cpf: CPF служащего (необязательно).
        nome: Имя служащего (необязательно, требует код органа).
        codigo_orgao_lotacao: Код SIAPE органа назначения (напр. "3" для AGU).
        codigo_orgao_exercicio: Код SIAPE органа фактической работы.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными служащими.
    """
    if not cpf and not codigo_orgao_lotacao and not codigo_orgao_exercicio:
        return (
            "Informe CPF ou código de órgão (lotação ou exercício) para a busca. "
            "A API exige pelo menos um desses filtros. "
            "Exemplos de códigos SIAPE: '3' (AGU), '26246' (UFPI), '25000' (MEC)."
        )

    servidores = await client.buscar_servidores(
        cpf=cpf,
        nome=nome,
        codigo_orgao_lotacao=codigo_orgao_lotacao,
        codigo_orgao_exercicio=codigo_orgao_exercicio,
        pagina=pagina,
    )
    if not servidores:
        busca = cpf or nome
        return f"Nenhum servidor encontrado para '{busca}'."

    rows = [
        (
            s.cpf or "—",
            (s.nome or "—")[:50],
            s.tipo_servidor or "—",
            s.situacao or "—",
            (s.orgao or "—")[:40],
        )
        for s in servidores
    ]
    busca = cpf or nome
    header = f"Servidores encontrados para '{busca}' (página {pagina}):\n\n"
    table = header + markdown_table(["CPF", "Nome", "Tipo", "Situação", "Órgão"], rows)
    return table + _pagination_hint(len(servidores), pagina)


async def buscar_licitacoes(
    codigo_orgao: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск федеральных торгов по органу и/или периоду.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Запрос тендерных процедур федерального правительства.

    Args:
        codigo_orgao: Код SIAFI органа (напр. "26246" для UFPI).
        data_inicial: Дата начала в формате DD/MM/YYYY.
        data_final: Дата окончания в формате DD/MM/YYYY.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными торгами.
    """
    licitacoes = await client.buscar_licitacoes(
        codigo_orgao=codigo_orgao,
        data_inicial=data_inicial,
        data_final=data_final,
        pagina=pagina,
    )
    if not licitacoes:
        return "Nenhuma licitação encontrada para os parâmetros informados."

    rows = [
        (
            lc.numero or "—",
            (lc.objeto or "—")[:60],
            lc.modalidade or "—",
            lc.situacao or "—",
            format_rub(lc.valor_estimado) if lc.valor_estimado else "—",
            lc.data_abertura or "—",
        )
        for lc in licitacoes
    ]
    header = f"Licitações encontradas (página {pagina}):\n\n"
    table = header + markdown_table(
        ["Número", "Objeto", "Modalidade", "Situação", "Valor Est.", "Abertura"], rows
    )
    return table + _pagination_hint(len(licitacoes), pagina)


async def consultar_bolsa_familia(
    mes_ano: str,
    codigo_ibge: str | None = None,
    nis: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Запрос данных программы Bolsa Família по муниципалитету или NIS.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Укажите код IBGE муниципалитета ИЛИ NIS получателя.
    Возвращает данные о выплатах программы социальной поддержки.

    Args:
        mes_ano: Месяц/год в формате YYYYMM (напр.: 202401).
        codigo_ibge: Код IBGE муниципалитета (напр.: 3550308 для Сан-Паулу).
        nis: NIS (Номер социальной идентификации) получателя.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Найденные данные Bolsa Família.
    """
    if not codigo_ibge and not nis:
        return "Informe o código IBGE do município ou o NIS do beneficiário."

    if nis:
        sacados = await client.consultar_bolsa_familia_nis(mes_ano, nis, pagina)
        if not sacados:
            return f"Nenhum dado encontrado para NIS '{nis}' em {mes_ano}."
        rows = [
            (
                s.nis or "—",
                (s.nome or "—")[:50],
                s.municipio or "—",
                s.uf or "—",
                format_rub(s.valor) if s.valor else "—",
            )
            for s in sacados
        ]
        table = f"Bolsa Família — NIS {nis} ({mes_ano}):\n\n" + markdown_table(
            ["NIS", "Nome", "Município", "UF", "Valor"], rows
        )
        return table + _pagination_hint(len(sacados), pagina)

    assert codigo_ibge is not None
    municipios = await client.consultar_bolsa_familia_municipio(mes_ano, codigo_ibge, pagina)
    if not municipios:
        return f"Nenhum dado encontrado para município {codigo_ibge} em {mes_ano}."
    rows = [
        (
            m.municipio or "—",
            m.uf or "—",
            str(m.quantidade) if m.quantidade else "—",
            format_rub(m.valor) if m.valor else "—",
            m.data_referencia or "—",
        )
        for m in municipios
    ]
    table = f"Bolsa Família — Município {codigo_ibge} ({mes_ano}):\n\n" + markdown_table(
        ["Município", "UF", "Beneficiados", "Valor", "Referência"], rows
    )
    return table + _pagination_hint(len(municipios), pagina)


async def buscar_sancoes(
    consulta: str,
    bases: list[str] | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск санкций в федеральных реестрах (CEIS, CNEP, CEPIM, CEAF).

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Одновременный запрос реестров санкций федерального правительства.
    Полезно для проверки добросовестности (due diligence) и антикоррупционного контроля.

    Доступные реестры:
    - CEIS: Недобросовестные и приостановленные компании
    - CNEP: Наказанные компании (Антикоррупционный закон 12.846)
    - CEPIM: Некоммерческие организации с ограничениями
    - CEAF: Исключения из Федеральной администрации

    Args:
        consulta: CPF, CNPJ или имя лица/компании для поиска.
        bases: Список реестров (напр., ["ceis", "cnep"]). По умолчанию: все.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Найденные санкции, сгруппированные по реестрам.
    """
    sancoes = await client.buscar_sancoes(consulta, bases, pagina)
    if not sancoes:
        bases_str = ", ".join(bases) if bases else "CEIS, CNEP, CEPIM, CEAF"
        return f"Nenhuma sanção encontrada para '{consulta}' nas bases: {bases_str}."

    items: list[str] = []
    for s in sancoes:
        parts = [f"**{s.nome or '—'}** ({s.cpf_cnpj or '—'})"]
        parts.append(f"  Fonte: {s.fonte or '—'}")
        if s.tipo:
            parts.append(f"  Tipo: {s.tipo}")
        if s.orgao:
            parts.append(f"  Órgão sancionador: {s.orgao}")
        if s.data_inicio or s.data_fim:
            parts.append(f"  Período: {s.data_inicio or '—'} a {s.data_fim or '—'}")
        if s.fundamentacao:
            parts.append(f"  Fundamentação: {s.fundamentacao}")
        items.append("\n".join(parts))

    header = f"Sanções encontradas para '{consulta}' ({len(sancoes)} resultado(s)):\n\n"
    result = header + truncate_list(items, max_items=30)
    return result + _pagination_hint(len(sancoes), pagina)


async def buscar_emendas(
    ano: int | None = None,
    nome_autor: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск парламентских поправок по году и/или автору.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Запрос индивидуальных и банковских поправок к федеральному бюджету.

    Args:
        ano: Год поправки (напр.: 2024).
        nome_autor: Имя парламентария — автора поправки.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными поправками.
    """
    emendas = await client.buscar_emendas(ano=ano, nome_autor=nome_autor, pagina=pagina)
    if not emendas:
        return "Nenhuma emenda encontrada para os parâmetros informados."

    rows = [
        (
            e.numero or "—",
            (e.autor or "—")[:40],
            e.tipo or "—",
            (e.localidade or "—")[:30],
            format_rub(e.valor_empenhado) if e.valor_empenhado else "—",
            format_rub(e.valor_pago) if e.valor_pago else "—",
        )
        for e in emendas
    ]
    header = f"Emendas parlamentares (página {pagina}):\n\n"
    table = header + markdown_table(
        ["Número", "Autor", "Tipo", "Localidade", "Empenhado", "Pago"], rows
    )
    return table + _pagination_hint(len(emendas), pagina)


async def consultar_viagens(cpf: str, pagina: int = 1) -> str:
    """(legacy) Запрос служебных поездок федерального служащего по CPF.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Показывает служебные поездки, включая суточные и транспорт.

    Args:
        cpf: CPF служащего (с форматированием или без).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными поездками.
    """
    viagens = await client.consultar_viagens(cpf, pagina)
    if not viagens:
        return f"Nenhuma viagem encontrada para o CPF '{cpf}'."

    rows = [
        (
            (v.nome or "—")[:40],
            v.cargo or "—",
            (v.orgao or "—")[:30],
            v.destino or "—",
            f"{v.data_inicio or '—'} a {v.data_fim or '—'}",
            format_rub(v.valor_diarias) if v.valor_diarias else "—",
            format_rub(v.valor_passagens) if v.valor_passagens else "—",
        )
        for v in viagens
    ]
    header = f"Viagens do servidor CPF {cpf} (página {pagina}):\n\n"
    table = header + markdown_table(
        ["Nome", "Cargo", "Órgão", "Destino", "Período", "Diárias", "Passagens"], rows
    )
    return table + _pagination_hint(len(viagens), pagina)


async def buscar_convenios(
    orgao: str | None = None,
    convenente: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск соглашений и добровольных трансферов федерального правительства.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Запрос соглашений между федеральными органами и организациями
    (штаты, муниципалитеты, НКО) для передачи ресурсов.

    Args:
        orgao: Код органа-грантодателя (напр. "26246").
        convenente: Название или CNPJ организации-партнёра.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными соглашениями.
    """
    convenios = await client.buscar_convenios(orgao=orgao, convenente=convenente, pagina=pagina)
    if not convenios:
        return "Nenhum convênio encontrado para os parâmetros informados."

    rows = [
        (
            c.numero or "—",
            (c.objeto or "—")[:60],
            c.situacao or "—",
            format_rub(c.valor_convenio) if c.valor_convenio else "—",
            format_rub(c.valor_liberado) if c.valor_liberado else "—",
            (c.orgao or "—")[:30],
            (c.convenente or "—")[:30],
        )
        for c in convenios
    ]
    header = f"Convênios encontrados (página {pagina}):\n\n"
    table = header + markdown_table(
        ["Número", "Objeto", "Situação", "Valor", "Liberado", "Órgão", "Convenente"], rows
    )
    return table + _pagination_hint(len(convenios), pagina)


async def buscar_cartoes_pagamento(
    cpf_portador: str | None = None,
    codigo_orgao: str | None = None,
    mes_ano_inicio: str | None = None,
    mes_ano_fim: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск платежей по корпоративным картам (авансовое обеспечение).

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Запрос расходов по корпоративным картам федерального правительства.

    Args:
        cpf_portador: CPF держателя карты (необязательно).
        codigo_orgao: Код органа (необязательно).
        mes_ano_inicio: Месяц/год начала в формате MM/YYYY (напр.: 01/2024).
        mes_ano_fim: Месяц/год окончания в формате MM/YYYY (напр.: 12/2024).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными платежами.
    """
    cartoes = await client.buscar_cartoes_pagamento(
        cpf_portador=cpf_portador,
        codigo_orgao=codigo_orgao,
        mes_ano_inicio=mes_ano_inicio,
        mes_ano_fim=mes_ano_fim,
        pagina=pagina,
    )
    if not cartoes:
        return "Nenhum pagamento com cartão encontrado para os parâmetros informados."

    rows = [
        (
            (c.portador or "—")[:40],
            (c.orgao or "—")[:30],
            format_rub(c.valor) if c.valor else "—",
            c.data or "—",
            c.tipo or "—",
            (c.estabelecimento or "—")[:30],
        )
        for c in cartoes
    ]
    header = f"Pagamentos com cartão (página {pagina}):\n\n"
    table = header + markdown_table(
        ["Portador", "Órgão", "Valor", "Data", "Tipo", "Estabelecimento"], rows
    )
    return table + _pagination_hint(len(cartoes), pagina)


async def buscar_pep(
    cpf: str | None = None,
    nome: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск политически значимых лиц (PEP).

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Запрос базы данных PEP федерального правительства — лиц, занимающих
    или занимавших значимые государственные должности.

    Args:
        cpf: CPF лица (необязательно, если указано имя).
        nome: Имя лица (необязательно, если указан CPF).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными PEP.
    """
    if not cpf and not nome:
        return "Informe CPF ou nome para buscar Pessoas Expostas Politicamente."

    peps = await client.buscar_pep(cpf=cpf, nome=nome, pagina=pagina)
    if not peps:
        busca = cpf or nome
        return f"Nenhuma PEP encontrada para '{busca}'."

    rows = [
        (
            p.cpf or "—",
            (p.nome or "—")[:40],
            (p.orgao or "—")[:30],
            p.funcao or "—",
            p.data_inicio or "—",
            p.data_fim or "—",
        )
        for p in peps
    ]
    busca = cpf or nome
    header = f"PEPs encontradas para '{busca}' (página {pagina}):\n\n"
    table = header + markdown_table(["CPF", "Nome", "Órgão", "Função", "Início", "Fim"], rows)
    return table + _pagination_hint(len(peps), pagina)


async def buscar_acordos_leniencia(
    nome_empresa: str | None = None,
    cnpj: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск соглашений о снисхождении (антикоррупция).

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Запрос соглашений с компаниями, вовлечёнными в противоправные действия
    против публичной администрации (Антикоррупционный закон 12.846/2013).

    Args:
        nome_empresa: Название компании (необязательно).
        cnpj: CNPJ компании (необязательно).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными соглашениями.
    """
    acordos = await client.buscar_acordos_leniencia(
        nome_empresa=nome_empresa, cnpj=cnpj, pagina=pagina
    )
    if not acordos:
        return "Nenhum acordo de leniência encontrado para os parâmetros informados."

    rows = [
        (
            (a.empresa or "—")[:40],
            a.cnpj or "—",
            (a.orgao or "—")[:30],
            a.situacao or "—",
            a.data_inicio or "—",
            format_rub(a.valor) if a.valor else "—",
        )
        for a in acordos
    ]
    header = f"Acordos de leniência (página {pagina}):\n\n"
    table = header + markdown_table(
        ["Empresa", "CNPJ", "Órgão", "Situação", "Início", "Valor Multa"], rows
    )
    return table + _pagination_hint(len(acordos), pagina)


async def buscar_notas_fiscais(
    cnpj_emitente: str | None = None,
    data_emissao_de: str | None = None,
    data_emissao_ate: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск электронных счетов-фактур, связанных с федеральными расходами.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Запрос электронных счетов-фактур, связанных с расходами федерального правительства.

    Args:
        cnpj_emitente: CNPJ эмитента счета (необязательно).
        data_emissao_de: Дата выставления начала DD/MM/YYYY (необязательно).
        data_emissao_ate: Дата выставления окончания DD/MM/YYYY (необязательно).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными счетами-фактурами.
    """
    notas = await client.buscar_notas_fiscais(
        cnpj_emitente=cnpj_emitente,
        data_emissao_de=data_emissao_de,
        data_emissao_ate=data_emissao_ate,
        pagina=pagina,
    )
    if not notas:
        return "Nenhuma nota fiscal encontrada para os parâmetros informados."

    rows = [
        (
            n.numero or "—",
            n.serie or "—",
            (n.emitente or "—")[:40],
            n.cnpj_emitente or "—",
            format_rub(n.valor) if n.valor else "—",
            n.data_emissao or "—",
        )
        for n in notas
    ]
    header = f"Notas fiscais (página {pagina}):\n\n"
    table = header + markdown_table(
        ["Número", "Série", "Emitente", "CNPJ", "Valor", "Emissão"], rows
    )
    return table + _pagination_hint(len(notas), pagina)


async def consultar_beneficio_social(
    cpf: str | None = None,
    nis: str | None = None,
    mes_ano: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Запрос социальных пособий (BPC, пособие по безработице и др.) по CPF или NIS.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Запрос социальных программ федерального правительства, помимо Bolsa Família.

    Args:
        cpf: CPF получателя (необязательно, если указан NIS).
        nis: NIS получателя (необязательно, если указан CPF).
        mes_ano: Месяц/год в формате YYYYMM (напр.: 202401).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными пособиями.
    """
    if not cpf and not nis:
        return "Informe CPF ou NIS do beneficiário."

    beneficios = await client.consultar_beneficio_social(
        cpf=cpf, nis=nis, mes_ano=mes_ano, pagina=pagina
    )
    if not beneficios:
        busca = cpf or nis
        return f"Nenhum benefício social encontrado para '{busca}'."

    rows = [
        (
            b.tipo or "—",
            (b.nome_beneficiario or "—")[:40],
            format_rub(b.valor) if b.valor else "—",
            b.mes_referencia or "—",
            b.municipio or "—",
            b.uf or "—",
        )
        for b in beneficios
    ]
    busca = cpf or nis
    header = f"Benefícios sociais para '{busca}' (página {pagina}):\n\n"
    table = header + markdown_table(
        ["Tipo", "Beneficiário", "Valor", "Referência", "Município", "UF"], rows
    )
    return table + _pagination_hint(len(beneficios), pagina)


async def consultar_cpf(cpf: str, pagina: int = 1) -> str:
    """(legacy) Запрос связей и пособий физического лица по CPF.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Показывает консолидированную информацию о связях лица
    с федеральным правительством (служащие, получатели, поставщики).

    Args:
        cpf: CPF лица (с форматированием или без).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Информация о найденных связях.
    """
    vinculos = await client.consultar_cpf(cpf, pagina)
    if not vinculos:
        return f"Nenhum vínculo encontrado para o CPF '{cpf}'."

    items: list[str] = []
    for v in vinculos:
        parts = [f"**{v.nome or '—'}** (CPF: {v.cpf or '—'})"]
        if v.tipo_vinculo:
            parts.append(f"  Tipo: {v.tipo_vinculo}")
        if v.orgao:
            parts.append(f"  Órgão: {v.orgao}")
        if v.beneficios:
            parts.append(f"  Benefícios: {v.beneficios}")
        items.append("\n".join(parts))

    header = f"Vínculos do CPF {cpf} ({len(vinculos)} resultado(s), página {pagina}):\n\n"
    result = header + truncate_list(items, max_items=30)
    return result + _pagination_hint(len(vinculos), pagina)


async def consultar_cnpj(cnpj: str, pagina: int = 1) -> str:
    """(legacy) Запрос санкций и контрактов юридического лица по CNPJ.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Показывает консолидированную информацию о компании
    при федеральном правительстве (контракты, санкции, задолженности).

    Args:
        cnpj: CNPJ компании (с форматированием или без).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Информация о найденных связях.
    """
    try:
        vinculos = await client.consultar_cnpj(cnpj, pagina)
    except HttpClientError as exc:
        if "403" in str(exc):
            return (
                f"Acesso negado ao consultar CNPJ '{cnpj}'. "
                "A chave API pode não ter permissão para o endpoint de pessoas jurídicas. "
                "Verifique as permissões em portaldatransparencia.gov.br."
            )
        return f"Erro ao consultar CNPJ '{cnpj}': {exc}"
    if not vinculos:
        return f"Nenhum vínculo encontrado para o CNPJ '{cnpj}'."

    items: list[str] = []
    for v in vinculos:
        parts = [f"**{v.razao_social or '—'}** (CNPJ: {v.cnpj or '—'})"]
        if v.sancoes:
            parts.append(f"  Sanções: {v.sancoes}")
        if v.contratos:
            parts.append(f"  Contratos: {v.contratos}")
        items.append("\n".join(parts))

    header = f"Vínculos do CNPJ {cnpj} ({len(vinculos)} resultado(s), página {pagina}):\n\n"
    result = header + truncate_list(items, max_items=30)
    return result + _pagination_hint(len(vinculos), pagina)


async def detalhar_contrato(id_contrato: int) -> str:
    """(legacy) Подробная информация о конкретном федеральном контракте.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Возвращает полную информацию: modalidade, тендер, статус и суммы.

    Args:
        id_contrato: ID контракта на Портале прозрачности.

    Returns:
        Детали контракта.
    """
    contrato = await client.detalhar_contrato(id_contrato)
    if not contrato:
        return f"Contrato com ID {id_contrato} não encontrado."

    lines = [
        f"## Contrato {contrato.numero or id_contrato}\n",
        f"- **Objeto:** {contrato.objeto or '—'}",
        f"- **Fornecedor:** {contrato.fornecedor or '—'}",
        f"- **Órgão:** {contrato.orgao or '—'}",
        f"- **Modalidade:** {contrato.modalidade or '—'}",
        f"- **Situação:** {contrato.situacao or '—'}",
        f"- **Valor Inicial:** "
        f"{format_rub(contrato.valor_inicial) if contrato.valor_inicial else '—'}",
        f"- **Valor Final:** {format_rub(contrato.valor_final) if contrato.valor_final else '—'}",
        f"- **Vigência:** {contrato.data_inicio or '—'} a {contrato.data_fim or '—'}",
        f"- **Licitação:** {contrato.licitacao or '—'}",
    ]
    return "\n".join(lines)


async def detalhar_servidor(id_servidor: int) -> str:
    """(legacy) Подробная информация о федеральном служащем по ID, включая вознаграждение.

    Инструмент совместимости с Порталом прозрачности Бразилии.
    Возвращает полную информацию: должность, функция и размер вознаграждения.

    Args:
        id_servidor: ID служащего на Портале прозрачности.

    Returns:
        Детали служащего.
    """
    servidor = await client.detalhar_servidor(id_servidor)
    if not servidor:
        return f"Servidor com ID {id_servidor} não encontrado."

    lines = [
        f"## Servidor {servidor.nome or id_servidor}\n",
        f"- **CPF:** {servidor.cpf or '—'}",
        f"- **Tipo:** {servidor.tipo_servidor or '—'}",
        f"- **Situação:** {servidor.situacao or '—'}",
        f"- **Órgão:** {servidor.orgao or '—'}",
        f"- **Cargo:** {servidor.cargo or '—'}",
        f"- **Função:** {servidor.funcao or '—'}",
        f"- **Remuneração Básica:** "
        f"{format_rub(servidor.remuneracao_basica) if servidor.remuneracao_basica else '—'}",
    ]
    if servidor.honorarios:
        lines.append(f"- **Honorários Advocatícios:** {format_rub(servidor.honorarios)}")
    if servidor.outras_remuneracoes:
        lines.append(f"- **Outras Remunerações:** {format_rub(servidor.outras_remuneracoes)}")
    if servidor.jetons:
        lines.append(f"- **Jetons:** {format_rub(servidor.jetons)}")
    lines.append(
        "- **Remuneração Líquida:** "
        + (
            format_rub(servidor.remuneracao_apos_deducoes)
            if servidor.remuneracao_apos_deducoes
            else "—"
        )
    )
    return "\n".join(lines)
