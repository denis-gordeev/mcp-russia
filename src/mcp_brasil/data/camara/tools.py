"""Инструменты для работы с Палатой депутатов Бразилии (слой совместимости, legacy).

Примечание: это слой совместимости в рамках mcp-russia. Данные инструменты
предоставляют устаревший доступ к данным бразильской Палаты депутатов и
считаются переходными.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from mcp_brasil._shared.formatting import format_brl, markdown_table

from . import client
from .constants import DEFAULT_PAGE_SIZE


def _pagination_hint(count: int, pagina: int) -> str:
    """Возвращает подсказку о пагинации на основе количества результатов и текущей страницы."""
    if count >= DEFAULT_PAGE_SIZE:
        return f"\n\n> Use `pagina={pagina + 1}` para ver mais resultados."
    if pagina > 1 and count < DEFAULT_PAGE_SIZE:
        return "\n\n> Última página de resultados."
    return ""


async def listar_deputados(
    nome: str | None = None,
    sigla_partido: str | None = None,
    sigla_uf: str | None = None,
    legislatura: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Список действующих федеральных депутатов с фильтрами.

    Инструмент совместимости с API Палаты депутатов Бразилии.
    Запрос парламентариев текущего или предыдущих созывов.

    Args:
        nome: Фильтр по имени депутата (частичное совпадение).
        sigla_partido: Фильтр по партии (напр.: PT, PL, PSDB).
        sigla_uf: Фильтр по штату (напр.: SP, RJ, PI).
        legislatura: ID созыва (напр., 57 для 2023-2027). По умолчанию: текущий.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными депутатами.
    """
    deputados = await client.listar_deputados(
        nome=nome,
        sigla_partido=sigla_partido,
        sigla_uf=sigla_uf,
        legislatura=legislatura,
        pagina=pagina,
    )
    if not deputados:
        return "Nenhum deputado encontrado para os filtros informados."

    rows = [
        (
            str(d.id or "—"),
            (d.nome or "—")[:40],
            d.sigla_partido or "—",
            d.sigla_uf or "—",
            d.email or "—",
        )
        for d in deputados
    ]
    header = f"Deputados federais (página {pagina}):\n\n"
    table = header + markdown_table(["ID", "Nome", "Partido", "UF", "Email"], rows)
    return table + _pagination_hint(len(deputados), pagina)


async def buscar_deputado(deputado_id: int) -> str:
    """(legacy) Поиск данных федерального депутата по ID.

    Инструмент совместимости с API Палаты депутатов Бразилии.
    Возвращает полную информацию: имя, партия, штат, email и фото.

    Args:
        deputado_id: ID депутата в API Палаты (напр., 204554).

    Returns:
        Подробный профиль депутата.
    """
    dep = await client.obter_deputado(deputado_id)
    if not dep:
        return f"Deputado com ID {deputado_id} não encontrado."

    lines = [
        f"**{dep.nome or '—'}**",
        f"- Partido: {dep.sigla_partido or '—'}",
        f"- UF: {dep.sigla_uf or '—'}",
        f"- Email: {dep.email or '—'}",
        f"- Legislatura: {dep.legislatura or '—'}",
    ]
    if dep.foto:
        lines.append(f"- Foto: {dep.foto}")
    return "\n".join(lines)


async def buscar_proposicao(
    sigla_tipo: str | None = None,
    numero: int | None = None,
    ano: int | None = None,
    keywords: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск законодательных предложений (PL, PEC, MPV и др.).

    Инструмент совместимости с API Палаты депутатов Бразилии.
    Позволяет фильтровать по типу, номеру, году или ключевым словам в аннотации.

    Args:
        sigla_tipo: Тип предложения (напр.: PL, PEC, MPV, PLP, PDL).
        numero: Номер предложения.
        ano: Год предложения.
        keywords: Ключевые слова для поиска в аннотации.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными предложениями.
    """
    proposicoes = await client.buscar_proposicoes(
        sigla_tipo=sigla_tipo,
        numero=numero,
        ano=ano,
        keywords=keywords,
        pagina=pagina,
    )
    if not proposicoes:
        return "Nenhuma proposição encontrada para os filtros informados."

    rows = [
        (
            str(p.id or "—"),
            f"{p.sigla_tipo or '—'} {p.numero or '—'}/{p.ano or '—'}",
            (p.ementa or "—")[:120] + ("..." if p.ementa and len(p.ementa) > 120 else ""),
            p.data_apresentacao or "—",
            (p.situacao or "—")[:30],
        )
        for p in proposicoes
    ]
    header = f"Proposições encontradas (página {pagina}):\n\n"
    table = header + markdown_table(
        ["ID", "Proposição", "Ementa", "Apresentação", "Situação"], rows
    )
    hint = (
        "\n\n> Use `detalhar_proposicao(proposicao_id=ID)` para ver"
        " autor, ementa completa e status."
    )
    return table + hint + _pagination_hint(len(proposicoes), pagina)


async def detalhar_proposicao(proposicao_id: int) -> str:
    """(legacy) Подробная информация о законодательном предложении по ID.

    Инструмент совместимости с API Палаты депутатов Бразилии.
    Возвращает полную информацию: автор, аннотация, статус, режим рассмотрения
    и ссылка на полный текст. Используйте ID, полученный из buscar_proposicao.

    Args:
        proposicao_id: ID предложения в API Палаты.

    Returns:
        Полные детали предложения.
    """
    prop = await client.obter_proposicao(proposicao_id)
    if not prop:
        return f"Proposição com ID {proposicao_id} não encontrada."

    tipo_num = f"{prop.sigla_tipo or ''} {prop.numero or ''}/{prop.ano or ''}"
    lines = [
        f"**{tipo_num.strip()}** (ID: {prop.id})",
        "",
        f"**Ementa:** {prop.ementa or '—'}",
        "",
        f"- Autor: {prop.autor or '—'}",
    ]
    if prop.autor_partido or prop.autor_uf:
        partido_uf = "/".join(filter(None, [prop.autor_partido, prop.autor_uf]))
        lines.append(f"- Partido/UF do autor: {partido_uf}")
    lines.extend(
        [
            f"- Apresentação: {prop.data_apresentacao or '—'}",
            f"- Situação: {prop.situacao or '—'}",
            f"- Órgão: {prop.orgao_situacao or '—'}",
            f"- Regime: {prop.regime or '—'}",
        ]
    )
    if prop.url_inteiro_teor:
        lines.append(f"- Inteiro teor: {prop.url_inteiro_teor}")

    return "\n".join(lines)


async def consultar_tramitacao(proposicao_id: int) -> str:
    """(legacy) Запрос истории рассмотрения законодательного предложения.

    Инструмент совместимости с API Палаты депутатов Бразилии.
    Показывает историю прохождения, включая резолюции и органы.

    Args:
        proposicao_id: ID предложения в API Палаты.

    Returns:
        Список событий рассмотрения.
    """
    tramitacoes = await client.obter_tramitacoes(proposicao_id)
    if not tramitacoes:
        return f"Nenhuma tramitação encontrada para a proposição {proposicao_id}."

    rows = [
        (
            t.data or "—",
            (t.descricao or "—")[:60],
            t.orgao or "—",
            (t.situacao or "—")[:30],
        )
        for t in tramitacoes[:50]
    ]
    header = f"Tramitação da proposição {proposicao_id}:\n\n"
    table = header + markdown_table(["Data", "Descrição", "Órgão", "Situação"], rows)
    if len(tramitacoes) > 50:
        table += f"\n\n... e mais {len(tramitacoes) - 50} eventos de tramitação."
    return table


async def buscar_votacao(
    proposicao_id: int | None = None,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск поимённых голосований в пленарном зале или комиссиях.

    Инструмент совместимости с API Палаты депутатов Бразилии.
    Фильтрация по конкретному предложению или периоду дат.

    Args:
        proposicao_id: ID предложения для фильтрации голосований.
        data_inicio: Дата начала в формате YYYY-MM-DD.
        data_fim: Дата окончания в формате YYYY-MM-DD.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными голосованиями.
    """
    votacoes = await client.listar_votacoes(
        proposicao_id=proposicao_id,
        data_inicio=data_inicio,
        data_fim=data_fim,
        pagina=pagina,
    )
    if not votacoes:
        return "Nenhuma votação encontrada para os filtros informados."

    rows = [
        (
            (v.id or "—")[:20],
            v.data or "—",
            (v.descricao or "—")[:60],
            "Sim" if v.aprovacao else "Não" if v.aprovacao is not None else "—",
        )
        for v in votacoes
    ]
    header = f"Votações encontradas (página {pagina}):\n\n"
    table = header + markdown_table(["ID", "Data", "Descrição", "Aprovada"], rows)
    return table + _pagination_hint(len(votacoes), pagina)


async def votos_nominais(votacao_id: str) -> str:
    """(legacy) Запрос поимённых голосов конкретного голосования.

    Инструмент совместимости с API Палаты депутатов Бразилии.
    Показывает, как проголосовал каждый депутат (Да, Нет, Воздержался и т.д.).

    Args:
        votacao_id: ID голосования в API Палаты.

    Returns:
        Таблица с индивидуальными голосами депутатов.
    """
    votos = await client.obter_votos(votacao_id)
    if not votos:
        return f"Nenhum voto nominal encontrado para a votação '{votacao_id}'."

    rows = [
        (
            (v.deputado_nome or "—")[:40],
            v.partido or "—",
            v.uf or "—",
            v.voto or "—",
        )
        for v in votos
    ]
    header = f"Votos nominais da votação {votacao_id} ({len(votos)} votos):\n\n"
    table = header + markdown_table(["Deputado", "Partido", "UF", "Voto"], rows)
    return table


async def despesas_deputado(
    deputado_id: int,
    ano: int | None = None,
    mes: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Запрос расходов депутатского парламентского фонда (CEAP).

    Инструмент совместимости с API Палаты депутатов Бразилии.
    Показывает расходы на питание, транспорт, офис и т.д.

    Args:
        deputado_id: ID депутата в API Палаты.
        ano: Год расходов (напр.: 2024).
        mes: Месяц расходов (1-12).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с расходами депутата.
    """
    despesas = await client.listar_despesas(
        deputado_id=deputado_id,
        ano=ano,
        mes=mes,
        pagina=pagina,
    )
    if not despesas:
        return f"Nenhuma despesa encontrada para o deputado {deputado_id}."

    rows = [
        (
            (d.tipo_despesa or "—")[:40],
            (d.fornecedor or "—")[:30],
            format_brl(d.valor_liquido) if d.valor_liquido else "—",
            d.data_documento or "—",
            f"{d.mes or '—'}/{d.ano or '—'}",
        )
        for d in despesas
    ]
    header = f"Despesas do deputado {deputado_id} (página {pagina}):\n\n"
    table = header + markdown_table(
        ["Tipo", "Fornecedor", "Valor Líquido", "Data", "Período"], rows
    )
    return table + _pagination_hint(len(despesas), pagina)


async def agenda_legislativa(
    data_inicio: str | None = None,
    data_fim: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Запрос законодательной повестки Палаты (сессии, слушания, заседания).

    Инструмент совместимости с API Палаты депутатов Бразилии.

    Args:
        data_inicio: Дата начала в формате YYYY-MM-DD.
        data_fim: Дата окончания в формате YYYY-MM-DD.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с законодательными событиями.
    """
    eventos = await client.listar_eventos(
        data_inicio=data_inicio,
        data_fim=data_fim,
        pagina=pagina,
    )
    if not eventos:
        return "Nenhum evento encontrado para o período informado."

    rows = [
        (
            e.data_inicio or "—",
            (e.titulo or "—")[:30],
            (e.descricao or "—")[:50],
            e.situacao or "—",
            (e.orgaos or "—")[:20],
        )
        for e in eventos
    ]
    header = f"Agenda legislativa (página {pagina}):\n\n"
    table = header + markdown_table(["Data/Hora", "Tipo", "Descrição", "Situação", "Órgãos"], rows)
    return table + _pagination_hint(len(eventos), pagina)


async def buscar_comissoes(
    sigla: str | None = None,
    tipo: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск комиссий и законодательных органов Палаты.

    Инструмент совместимости с API Палаты депутатов Бразилии.
    Включает постоянные комиссии, временные комиссии, CPI и другие органы.

    Args:
        sigla: Аббревиатура комиссии (напр.: CCJC, CFT, CESP).
        tipo: Код типа органа (напр., постоянные комиссии).
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с найденными комиссиями.
    """
    orgaos = await client.listar_orgaos(sigla=sigla, tipo=tipo, pagina=pagina)
    if not orgaos:
        return "Nenhuma comissão/órgão encontrado para os filtros informados."

    rows = [
        (
            o.sigla or "—",
            (o.nome or "—")[:60],
            o.tipo or "—",
            o.situacao or "—",
        )
        for o in orgaos
    ]
    header = f"Comissões/órgãos da Câmara (página {pagina}):\n\n"
    table = header + markdown_table(["Sigla", "Nome", "Tipo", "Situação"], rows)
    return table + _pagination_hint(len(orgaos), pagina)


async def frentes_parlamentares(
    legislatura: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Список парламентских фронтов Палаты депутатов.

    Инструмент совместимости с API Палаты депутатов Бразилии.
    Парламентские фронты — надпартийные объединения депутатов
    для продвижения законодательства по конкретным темам.

    Args:
        legislatura: ID созыва (напр.: 57). По умолчанию: текущий.
        pagina: Страница результатов (по умолчанию: 1).

    Returns:
        Таблица с парламентскими фронтами.
    """
    frentes = await client.listar_frentes(legislatura=legislatura, pagina=pagina)
    if not frentes:
        return "Nenhuma frente parlamentar encontrada."

    rows = [
        (
            str(f.id or "—"),
            (f.titulo or "—")[:60],
            str(f.legislatura or "—"),
            (f.coordenador or "—")[:30],
        )
        for f in frentes
    ]
    header = f"Frentes parlamentares (página {pagina}):\n\n"
    table = header + markdown_table(["ID", "Título", "Legislatura", "Coordenador"], rows)
    return table + _pagination_hint(len(frentes), pagina)
