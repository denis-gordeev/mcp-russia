"""Инструменты для работы с Федеральным сенатом Бразилии (слой совместимости, legacy).

Примечание: это слой совместимости в рамках mcp-russia. Данные инструменты
предоставляют устаревший доступ к данным бразильского Федерального сената
и считаются переходными.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from mcp_russia._shared.formatting import markdown_table

from . import client
from .constants import DEFAULT_PAGE_SIZE


def _pagination_hint(count: int, page_size: int = DEFAULT_PAGE_SIZE) -> str:
    """Подсказка при наличии дополнительных результатов."""
    if count >= page_size:
        return "\n\n> Há mais resultados. Refine os filtros para resultados mais específicos."
    return ""


# --- Senadores (4 tools) ---------------------------------------------------


async def listar_senadores() -> str:
    """(legacy) Список всех действующих сенаторов Федерального сената.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает полный список сенаторов текущего созыва с партией и штатом.

    Returns:
        Таблица с действующими сенаторами.
    """
    senadores = await client.listar_senadores()
    if not senadores:
        return "Nenhum senador em exercício encontrado."

    rows = [
        (
            s.codigo or "—",
            (s.nome or "—")[:40],
            s.partido or "—",
            s.uf or "—",
        )
        for s in senadores
    ]
    header = f"Senadores em exercício ({len(senadores)} senadores):\n\n"
    return header + markdown_table(["Código", "Nome", "Partido", "UF"], rows)


async def buscar_senador(codigo: str) -> str:
    """(legacy) Поиск данных сенатора по коду.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает полный профиль: имя, партия, штат, контакты и мандат.

    Args:
        codigo: Код сенатора в API Сената.

    Returns:
        Подробный профиль сенатора.
    """
    sen = await client.obter_senador(codigo)
    if not sen:
        return f"Senador com código {codigo} não encontrado."

    lines = [
        f"**{sen.nome_completo or sen.nome or '—'}**",
        f"- Partido: {sen.partido or '—'}",
        f"- UF: {sen.uf or '—'}",
        f"- Email: {sen.email or '—'}",
        f"- Telefone: {sen.telefone or '—'}",
    ]
    if sen.mandato_inicio or sen.mandato_fim:
        lines.append(f"- Mandato: {sen.mandato_inicio or '—'} a {sen.mandato_fim or '—'}")
    if sen.foto:
        lines.append(f"- Foto: {sen.foto}")
    return "\n".join(lines)


async def buscar_senador_por_nome(nome: str) -> str:
    """(legacy) Поиск сенаторов по имени.

    Инструмент совместимости с API Сената Бразилии.
    Частичный поиск по именам сенаторов текущего созыва.

    Args:
        nome: Имя или часть имени сенатора.

    Returns:
        Таблица с найденными сенаторами.
    """
    senadores = await client.buscar_senador_por_nome(nome)
    if not senadores:
        return f"Nenhum senador encontrado com o nome '{nome}'."

    rows = [
        (
            s.codigo or "—",
            (s.nome or "—")[:40],
            s.partido or "—",
            s.uf or "—",
        )
        for s in senadores
    ]
    header = f"Senadores encontrados para '{nome}':\n\n"
    return header + markdown_table(["Código", "Nome", "Partido", "UF"], rows)


async def votacoes_senador(codigo: str) -> str:
    """(legacy) Запрос голосований, в которых участвовал сенатор.

    Инструмент совместимости с API Сената Бразилии.

    Args:
        codigo: Код сенатора в API Сената.

    Returns:
        Список голосований с датами и результатами.
    """
    votacoes = await client.votacoes_senador(codigo)
    if not votacoes:
        return f"Nenhuma votação encontrada para o senador {codigo}."

    rows = [
        (
            v.codigo or "—",
            v.data or "—",
            (v.descricao or "—")[:60],
            v.resultado or "—",
        )
        for v in votacoes[:50]
    ]
    header = f"Votações do senador {codigo} ({len(votacoes)} votações):\n\n"
    table = header + markdown_table(["Código", "Data", "Descrição", "Resultado"], rows)
    if len(votacoes) > 50:
        table += f"\n\n... e mais {len(votacoes) - 50} votações."
    return table


# --- Matérias (5 tools) ----------------------------------------------------


async def buscar_materia(
    sigla_tipo: str | None = None,
    numero: str | None = None,
    ano: str | None = None,
    keywords: str | None = None,
    tramitando: bool = False,
) -> str:
    """(legacy) Поиск законодательных материалов Сената (PEC, PLS, PLC, MPV и др.).

    Инструмент совместимости с API Сената Бразилии.
    Позволяет фильтровать по типу, номеру, году или ключевым словам.

    Args:
        sigla_tipo: Тип материала (напр.: PEC, PLS, PLC, MPV, PLP).
        numero: Номер материала.
        ano: Год материала.
        keywords: Ключевые слова для поиска в аннотации.
        tramitando: Если True, возвращает только материалы на рассмотрении.

    Returns:
        Таблица с найденными материалами.
    """
    materias = await client.buscar_materias(
        sigla_tipo=sigla_tipo,
        numero=numero,
        ano=ano,
        keywords=keywords,
        tramitando=tramitando,
    )
    if not materias:
        return "Nenhuma matéria encontrada para os filtros informados."

    rows = [
        (
            f"{m.sigla_tipo or '—'} {m.numero or '—'}/{m.ano or '—'}",
            (m.ementa or "—")[:80],
            m.data_apresentacao or "—",
            (m.situacao or "—")[:30],
        )
        for m in materias[:DEFAULT_PAGE_SIZE]
    ]
    header = f"Matérias encontradas ({len(materias)} resultado(s)):\n\n"
    table = header + markdown_table(["Matéria", "Ementa", "Apresentação", "Situação"], rows)
    return table + _pagination_hint(len(materias))


async def detalhe_materia(codigo: str) -> str:
    """(legacy) Получение детальной информации о законодательном материале по коду.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает полную аннотацию, автора, статус и палату происхождения.

    Args:
        codigo: Код материала в API Сената.

    Returns:
        Полные детали материала.
    """
    materia = await client.obter_materia(codigo)
    if not materia:
        return f"Matéria com código {codigo} não encontrada."

    ident = f"{materia.sigla_tipo or '—'} {materia.numero or '—'}/{materia.ano or '—'}"
    lines = [
        f"**{ident}**",
        f"- Ementa: {materia.ementa or '—'}",
    ]
    if materia.ementa_completa:
        lines.append(f"- Explicação: {materia.ementa_completa}")
    lines.extend(
        [
            f"- Autor: {materia.autor or '—'}",
            f"- Data de apresentação: {materia.data_apresentacao or '—'}",
            f"- Situação: {materia.situacao or '—'}",
            f"- Casa de origem: {materia.casa_origem or '—'}",
        ]
    )
    return "\n".join(lines)


async def consultar_tramitacao_materia(codigo: str) -> str:
    """(legacy) Запрос истории рассмотрения законодательного материала в Сенате.

    Инструмент совместимости с API Сената Бразилии.
    Показывает историю прохождения с датами, местами и статусами.

    Args:
        codigo: Код материала в API Сената.

    Returns:
        Список событий прохождения.
    """
    tramitacoes = await client.tramitacao_materia(codigo)
    if not tramitacoes:
        return f"Nenhuma tramitação encontrada para a matéria {codigo}."

    rows = [
        (
            t.data or "—",
            (t.descricao or "—")[:60],
            t.local or "—",
            (t.situacao or "—")[:30],
        )
        for t in tramitacoes[:50]
    ]
    header = f"Tramitação da matéria {codigo}:\n\n"
    table = header + markdown_table(["Data", "Descrição", "Local", "Situação"], rows)
    if len(tramitacoes) > 50:
        table += f"\n\n... e mais {len(tramitacoes) - 50} eventos de tramitação."
    return table


async def textos_materia(codigo: str) -> str:
    """(legacy) Список текстов и документов законодательного материала.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает ссылки на официальные документы (оригинальный текст, поправки, заключения).

    Args:
        codigo: Код материала в API Сената.

    Returns:
        Список документов с URL.
    """
    textos = await client.textos_materia(codigo)
    if not textos:
        return f"Nenhum texto encontrado para a matéria {codigo}."

    rows = [
        (
            t.get("tipo") or "—",
            t.get("data") or "—",
            t.get("url") or "—",
        )
        for t in textos
    ]
    header = f"Textos da matéria {codigo}:\n\n"
    return header + markdown_table(["Tipo", "Data", "URL"], rows)


async def votos_materia(codigo: str) -> str:
    """(legacy) Запрос голосований по законодательному материалу в Сенате.

    Инструмент совместимости с API Сената Бразилии.
    Показывает результаты с подсчётом (Да/Нет/Воздержался).

    Args:
        codigo: Код материала в API Сената.

    Returns:
        Список голосований с результатами.
    """
    votacoes = await client.votos_materia(codigo)
    if not votacoes:
        return f"Nenhuma votação encontrada para a matéria {codigo}."

    rows = [
        (
            v.codigo or "—",
            v.data or "—",
            (v.descricao or "—")[:50],
            v.resultado or "—",
            f"S:{v.sim or 0} N:{v.nao or 0} A:{v.abstencao or 0}",
        )
        for v in votacoes
    ]
    header = f"Votações da matéria {codigo}:\n\n"
    return header + markdown_table(["Código", "Data", "Descrição", "Resultado", "Placar"], rows)


# --- Votações (3 tools) ----------------------------------------------------


async def listar_votacoes(ano: str) -> str:
    """(legacy) Список голосований пленарного зала Сената за год.

    Инструмент совместимости с API Сената Бразилии.

    Args:
        ano: Год голосований (напр.: 2024).

    Returns:
        Таблица с голосованиями года.
    """
    votacoes = await client.listar_votacoes(ano)
    if not votacoes:
        return f"Nenhuma votação encontrada para o ano {ano}."

    rows = [
        (
            v.codigo or "—",
            v.data or "—",
            (v.descricao or "—")[:60],
            v.resultado or "—",
        )
        for v in votacoes[:DEFAULT_PAGE_SIZE]
    ]
    header = f"Votações do plenário em {ano} ({len(votacoes)} votações):\n\n"
    table = header + markdown_table(["Código", "Data", "Descrição", "Resultado"], rows)
    return table + _pagination_hint(len(votacoes))


async def detalhe_votacao(codigo_sessao: str) -> str:
    """(legacy) Получение детальной информации о голосовании Сената, включая подсчёт.

    Инструмент совместимости с API Сената Бразилии.

    Args:
        codigo_sessao: Код сессии голосования.

    Returns:
        Детали голосования с подсчётом.
    """
    votacao = await client.obter_votacao(codigo_sessao)
    if not votacao:
        return f"Votação com código {codigo_sessao} não encontrada."

    lines = [
        f"**Votação {votacao.codigo or '—'}**",
        f"- Data: {votacao.data or '—'}",
        f"- Descrição: {votacao.descricao or '—'}",
        f"- Resultado: {votacao.resultado or '—'}",
        f"- Placar: Sim={votacao.sim or 0}, Não={votacao.nao or 0}, "
        f"Abstenção={votacao.abstencao or 0}",
    ]
    if votacao.materia_descricao:
        lines.append(f"- Matéria: {votacao.materia_descricao}")
    return "\n".join(lines)


async def votacoes_recentes(data: str) -> str:
    """(legacy) Список голосований Сената за конкретную дату.

    Инструмент совместимости с API Сената Бразилии.

    Args:
        data: Дата в формате YYYYMMDD (напр.: 20240315).

    Returns:
        Таблица с голосованиями даты.
    """
    votacoes = await client.votacoes_recentes(data)
    if not votacoes:
        return f"Nenhuma votação encontrada para a data {data}."

    rows = [
        (
            v.codigo or "—",
            v.data or "—",
            (v.descricao or "—")[:60],
            v.resultado or "—",
        )
        for v in votacoes
    ]
    header = f"Votações em {data}:\n\n"
    return header + markdown_table(["Código", "Data", "Descrição", "Resultado"], rows)


# --- Comissões (4 tools) ---------------------------------------------------


async def listar_comissoes() -> str:
    """(legacy) Список комиссий Федерального сената.

    Инструмент совместимости с API Сената Бразилии.
    Включает постоянные комиссии, временные комиссии, CPI и подкомиссии.

    Returns:
        Таблица с комиссиями Сената.
    """
    comissoes = await client.listar_comissoes()
    if not comissoes:
        return "Nenhuma comissão encontrada."

    rows = [
        (
            c.codigo or "—",
            c.sigla or "—",
            (c.nome or "—")[:60],
            c.tipo or "—",
        )
        for c in comissoes
    ]
    header = f"Comissões do Senado ({len(comissoes)} comissões):\n\n"
    return header + markdown_table(["Código", "Sigla", "Nome", "Tipo"], rows)


async def detalhe_comissao(codigo: str) -> str:
    """(legacy) Получение детальной информации о комиссии Сената.

    Инструмент совместимости с API Сената Бразилии.

    Args:
        codigo: Код комиссии в API Сената.

    Returns:
        Детали комиссии.
    """
    comissao = await client.obter_comissao(codigo)
    if not comissao:
        return f"Comissão com código {codigo} não encontrada."

    lines = [
        f"**{comissao.nome or '—'}** ({comissao.sigla or '—'})",
        f"- Tipo: {comissao.tipo or '—'}",
        f"- Data de criação: {comissao.data_criacao or '—'}",
    ]
    if comissao.data_extincao:
        lines.append(f"- Data de extinção: {comissao.data_extincao}")
    if comissao.finalidade:
        lines.append(f"- Finalidade: {comissao.finalidade}")
    return "\n".join(lines)


async def membros_comissao(codigo: str) -> str:
    """(legacy) Список членов комиссии Сената.

    Инструмент совместимости с API Сената Бразилии.

    Args:
        codigo: Код комиссии в API Сената.

    Returns:
        Таблица с членами комиссии.
    """
    membros = await client.membros_comissao(codigo)
    if not membros:
        return f"Nenhum membro encontrado para a comissão {codigo}."

    rows = [
        (
            (m.nome or "—")[:40],
            m.partido or "—",
            m.uf or "—",
            m.cargo or "—",
        )
        for m in membros
    ]
    header = f"Membros da comissão {codigo}:\n\n"
    return header + markdown_table(["Nome", "Partido", "UF", "Cargo"], rows)


async def reunioes_comissao(codigo: str) -> str:
    """(legacy) Список заседаний комиссии Сената.

    Инструмент совместимости с API Сената Бразилии.

    Args:
        codigo: Код комиссии в API Сената.

    Returns:
        Таблица с заседаниями комиссии.
    """
    reunioes = await client.reunioes_comissao(codigo)
    if not reunioes:
        return f"Nenhuma reunião encontrada para a comissão {codigo}."

    rows = [
        (
            r.data or "—",
            r.tipo or "—",
            (r.pauta or "—")[:60],
            r.local or "—",
        )
        for r in reunioes[:DEFAULT_PAGE_SIZE]
    ]
    header = f"Reuniões da comissão {codigo}:\n\n"
    table = header + markdown_table(["Data", "Tipo", "Pauta", "Local"], rows)
    return table + _pagination_hint(len(reunioes))


# --- Agenda (2 tools) ------------------------------------------------------


async def agenda_plenario(ano: str, mes: str) -> str:
    """(legacy) Запрос повестки пленарного зала Сената на месяц.

    Инструмент совместимости с API Сената Бразилии.

    Args:
        ano: Год (напр.: 2024).
        mes: Месяц (01-12).

    Returns:
        Таблица с пленарными сессиями месяца.
    """
    sessoes = await client.agenda_plenario(ano, mes)
    if not sessoes:
        return f"Nenhuma sessão encontrada para {mes}/{ano}."

    rows = [
        (
            s.data or "—",
            s.tipo or "—",
            s.numero or "—",
            s.situacao or "—",
        )
        for s in sessoes
    ]
    header = f"Agenda do plenário — {mes}/{ano}:\n\n"
    return header + markdown_table(["Data", "Tipo", "Número", "Situação"], rows)


async def agenda_comissoes(data: str) -> str:
    """(legacy) Запрос повестки комиссий Сената на дату.

    Инструмент совместимости с API Сената Бразилии.

    Args:
        data: Дата в формате YYYYMMDD (напр.: 20240315).

    Returns:
        Таблица с заседаниями комиссий на дату.
    """
    reunioes = await client.agenda_comissoes(data)
    if not reunioes:
        return f"Nenhuma reunião de comissão encontrada para a data {data}."

    rows = [
        (
            r.data or "—",
            r.comissao or "—",
            r.tipo or "—",
            (r.pauta or "—")[:60],
        )
        for r in reunioes
    ]
    header = f"Reuniões de comissões em {data}:\n\n"
    return header + markdown_table(["Data", "Comissão", "Tipo", "Pauta"], rows)


# --- Auxiliares (2 tools) --------------------------------------------------


async def legislatura_atual() -> str:
    """(legacy) Запрос информации о текущем созыве Сената.

    Инструмент совместимости с API Сената Бразилии.

    Returns:
        Данные созыва (номер, период).
    """
    leg = await client.legislatura_atual()
    if not leg:
        return "Informação da legislatura não disponível."

    return (
        f"**Legislatura {leg.numero or '—'}**\n"
        f"- Início: {leg.data_inicio or '—'}\n"
        f"- Fim: {leg.data_fim or '—'}"
    )


async def partidos_senado() -> str:
    """(legacy) Список партий, представленных в Федеральном сенате.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает партии, отсортированные по количеству действующих сенаторов.

    Returns:
        Таблица с партиями и количеством сенаторов.
    """
    senadores = await client.listar_senadores()
    if not senadores:
        return "Nenhum senador encontrado."

    contagem: dict[str, int] = {}
    for s in senadores:
        partido = s.partido or "S/Partido"
        contagem[partido] = contagem.get(partido, 0) + 1

    rows = [(partido, str(qtd)) for partido, qtd in sorted(contagem.items(), key=lambda x: -x[1])]
    header = f"Partidos no Senado ({len(contagem)} partidos, {len(senadores)} senadores):\n\n"
    return header + markdown_table(["Partido", "Senadores"], rows)


async def ufs_senado() -> str:
    """(legacy) Список федеративных единиц, представленных в Федеральном сенате.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает штаты, отсортированные по аббревиатуре с количеством сенаторов.

    Returns:
        Таблица с UF и количеством сенаторов.
    """
    senadores = await client.listar_senadores()
    if not senadores:
        return "Nenhum senador encontrado."

    contagem: dict[str, int] = {}
    for s in senadores:
        uf = s.uf or "N/A"
        contagem[uf] = contagem.get(uf, 0) + 1

    rows = [(uf, str(qtd)) for uf, qtd in sorted(contagem.items())]
    header = f"UFs no Senado ({len(contagem)} UFs, {len(senadores)} senadores):\n\n"
    return header + markdown_table(["UF", "Senadores"], rows)


async def tipos_materia() -> str:
    """(legacy) Список типов законодательных материалов Сената.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает аббревиатуры и описания основных типов предложений.

    Returns:
        Таблица с типами материалов.
    """
    tipos = await client.tipos_materia_api()
    rows = [(sigla, descricao) for sigla, descricao in sorted(tipos.items())]
    return "Tipos de matéria do Senado:\n\n" + markdown_table(["Sigla", "Descrição"], rows)


# --- Dados Abertos Extras (4 tools) ------------------------------------------


async def emendas_materia(codigo: str) -> str:
    """(legacy) Список поправок к законодательному материалу Сената.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает поправки с автором, типом, решением и ссылкой на документ.

    Args:
        codigo: Код материала в API Сената.

    Returns:
        Таблица с поправками материала.
    """
    emendas = await client.emendas_materia(codigo)
    if not emendas:
        return f"Nenhuma emenda encontrada para a matéria {codigo}."

    rows = [
        (
            e.numero or "—",
            (e.tipo or "—")[:30],
            (e.autor or "—")[:30],
            (e.decisao or "—")[:30],
            e.data_apresentacao or "—",
        )
        for e in emendas[:DEFAULT_PAGE_SIZE]
    ]
    header = f"Emendas da matéria {codigo} ({len(emendas)} emenda(s)):\n\n"
    table = header + markdown_table(["Número", "Tipo", "Autor", "Decisão", "Apresentação"], rows)
    return table + _pagination_hint(len(emendas))


async def listar_blocos() -> str:
    """(legacy) Список парламентских блоков (коалиций) Федерального сената.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает активные блоки с входящими партиями.

    Returns:
        Таблица с парламентскими блоками.
    """
    blocos = await client.listar_blocos()
    if not blocos:
        return "Nenhum bloco parlamentar encontrado."

    rows = [
        (
            b.codigo or "—",
            (b.nome or "—")[:40],
            b.apelido or "—",
            b.data_criacao or "—",
            ", ".join(b.partidos) if b.partidos else "—",
        )
        for b in blocos
    ]
    header = f"Blocos parlamentares do Senado ({len(blocos)} bloco(s)):\n\n"
    return header + markdown_table(["Código", "Nome", "Apelido", "Criação", "Partidos"], rows)


async def listar_liderancas() -> str:
    """(legacy) Список руководств Федерального сената.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает лидеров партий, блоков и правительства с их должностями.

    Returns:
        Таблица с руководствами Сената.
    """
    liderancas = await client.listar_liderancas()
    if not liderancas:
        return "Nenhuma liderança encontrada."

    rows = [
        (
            (lid.nome_parlamentar or "—")[:30],
            lid.partido or "—",
            (lid.tipo_lideranca or "—")[:25],
            (lid.unidade_lideranca or "—")[:25],
            lid.data_designacao or "—",
        )
        for lid in liderancas
    ]
    header = f"Lideranças do Senado ({len(liderancas)} liderança(s)):\n\n"
    return header + markdown_table(["Nome", "Partido", "Tipo", "Unidade", "Designação"], rows)


async def relatorias_senador(codigo: str) -> str:
    """(legacy) Запрос материалов, по которым сенатор назначен докладчиком.

    Инструмент совместимости с API Сената Бразилии.
    Возвращает материалы, для которых сенатор был назначен докладчиком.

    Args:
        codigo: Код сенатора в API Сената.

    Returns:
        Таблица с докладчиками сенатора.
    """
    relatorias = await client.relatorias_senador(codigo)
    if not relatorias:
        return f"Nenhuma relatoria encontrada para o senador {codigo}."

    rows = [
        (
            r.codigo_materia or "—",
            (r.identificacao or "—")[:30],
            (r.ementa or "—")[:50],
            (r.tipo_relator or "—")[:20],
            r.colegiado or "—",
        )
        for r in relatorias[:DEFAULT_PAGE_SIZE]
    ]
    header = f"Relatorias do senador {codigo} ({len(relatorias)} relatoria(s)):\n\n"
    table = header + markdown_table(
        ["Cód. Matéria", "Identificação", "Ementa", "Tipo Relator", "Colegiado"], rows
    )
    return table + _pagination_hint(len(relatorias))
