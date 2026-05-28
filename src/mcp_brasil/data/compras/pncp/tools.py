"""Tool functions for the PNCP feature.

Инструмент совместимости с API Национального портала государственных закупок Бразилии (PNCP).
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM

ВАЖНО: API PNCP НЕ поддерживает параметр текстового поиска.
Вся текстовая фильтрация выполняется на стороне клиента после получения результатов.
Формат дат для всех эндпоинтов: YYYYMMDD (также принимает YYYY-MM-DD и DD/MM/YYYY).
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_rub

from . import client
from .constants import MODALIDADES


async def buscar_contratacoes(
    data_inicial: str,
    data_final: str,
    modalidade: int,
    ctx: Context,
    texto: str | None = None,
    uf: str | None = None,
    cnpj_orgao: str | None = None,
    modo_disputa: int | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск государственных закупок и контрактов в PNCP по периоду и модальности.

    Примечание: инструмент совместимости для бразильских данных PNCP.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск в Национальном портале государственных закупок (Закон 14.133/2021).
    Охватывает федеральные, региональные и муниципальные закупки.

    ВАЖНО: API PNCP не поддерживает текстовый поиск. Параметр 'texto'
    фильтрует результаты локально после запроса API.

    Args:
        data_inicial: Начальная дата в формате YYYYMMDD (напр.: 20250101).
            Также принимает YYYY-MM-DD или DD/MM/YYYY.
        data_final: Конечная дата в формате YYYYMMDD (напр.: 20250331).
            Максимум 365 дней между датами.
        modalidade: Код модальности закупки (обязательно).
            Основные: 6=Электронный аукцион, 8=Отказ, 9=Необязательность,
            4=Электронный конкурс, 12=Аккредитация.
            Используйте ресурс 'data://modalidades' для просмотра всех кодов.
        texto: Локальный текстовый фильтр (необязательно). Фильтрует по объекту, органу
            или поставщику ПОСЛЕ получения результатов API.
        uf: Аббревиатура штата органа-заказчика (напр.: SP, RJ, DF). Необязательно.
        cnpj_orgao: CNPJ органа-заказчика (необязательно).
        modo_disputa: Код режима торгов (необязательно).
            1=Открытый, 2=Закрытый, 3=Открыто-Закрытый, 4=Отказ с торгами.
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных закупок с объектом, стоимостью и статусом.
    """
    mod_nome = MODALIDADES.get(modalidade, f"Código {modalidade}")
    await ctx.info(f"Buscando contratações ({mod_nome})...")

    try:
        resultado = await client.buscar_contratacoes(
            data_inicial=data_inicial,
            data_final=data_final,
            modalidade=modalidade,
            texto=texto,
            uf=uf,
            cnpj_orgao=cnpj_orgao,
            modo_disputa=modo_disputa,
            pagina=pagina,
        )
    except ValueError as e:
        return f"Erro de validação: {e}"

    await ctx.info(f"{resultado.total} contratações encontradas")

    if not resultado.contratacoes:
        filtro = f" contendo '{texto}'" if texto else ""
        return (
            f"Nenhuma contratação encontrada para {mod_nome} "
            f"entre {data_inicial} e {data_final}{filtro}."
        )

    lines = [f"**Total:** {resultado.total} contratações\n"]
    for i, c in enumerate(resultado.contratacoes, 1):
        modalidade_desc = MODALIDADES.get(c.modalidade_id or 0, c.modalidade_nome or "N/A")
        valor_est = format_rub(c.valor_estimado) if c.valor_estimado else "N/A"
        valor_hom = format_rub(c.valor_homologado) if c.valor_homologado else "N/A"
        lines.extend(
            [
                f"### {i}. {c.objeto or 'Sem descrição'}",
                f"**Órgão:** {c.orgao_nome or 'N/A'} ({c.orgao_cnpj or 'N/A'})",
                f"**Modalidade:** {modalidade_desc}",
                f"**Situação:** {c.situacao_nome or 'N/A'}",
                f"**Valor estimado:** {valor_est} | **Homologado:** {valor_hom}",
                f"**Publicação:** {c.data_publicacao or 'N/A'}",
                f"**Local:** {c.municipio or 'N/A'}/{c.uf or 'N/A'} ({c.esfera or 'N/A'})",
            ]
        )
        if c.link_pncp:
            lines.append(f"[Ver no PNCP]({c.link_pncp})")
        lines.append("")

    if texto:
        lines.append(f"*Filtrado localmente por '{texto}'.*")
    if resultado.total > len(resultado.contratacoes):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)


async def buscar_contratos(
    data_inicial: str,
    data_final: str,
    ctx: Context,
    texto: str | None = None,
    cnpj_orgao: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск государственных контрактов в PNCP по периоду.

    Примечание: инструмент совместимости для бразильских данных PNCP.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает контракты, опубликованные в Национальном портале государственных закупок.

    ВАЖНО: API PNCP не поддерживает текстовый поиск в контрактах.
    Параметр 'texto' фильтрует результаты локально.

    Args:
        data_inicial: Начальная дата в формате YYYYMMDD (напр.: 20250101).
            Также принимает YYYY-MM-DD или DD/MM/YYYY.
        data_final: Конечная дата в формате YYYYMMDD (напр.: 20250331).
            Максимум 365 дней между датами.
        texto: Локальный текстовый фильтр (необязательно). Фильтрует по объекту,
            органу или поставщику ПОСЛЕ получения результатов API.
        cnpj_orgao: CNPJ органа-заказчика (необязательно).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных контрактов.
    """
    await ctx.info(f"Buscando contratos ({data_inicial} a {data_final})...")

    try:
        resultado = await client.buscar_contratos(
            data_inicial=data_inicial,
            data_final=data_final,
            texto=texto,
            cnpj_orgao=cnpj_orgao,
            pagina=pagina,
        )
    except ValueError as e:
        return f"Erro de validação: {e}"

    await ctx.info(f"{resultado.total} contratos encontrados")

    if not resultado.contratos:
        filtro = f" contendo '{texto}'" if texto else ""
        return f"Nenhum contrato encontrado entre {data_inicial} e {data_final}{filtro}."

    lines = [f"**Total:** {resultado.total} contratos\n"]
    for i, c in enumerate(resultado.contratos, 1):
        raw_valor = c.valor_final or c.valor_inicial
        valor = format_rub(raw_valor) if raw_valor else "N/A"
        lines.extend(
            [
                f"### {i}. {c.objeto or 'Sem descrição'}",
                f"**Órgão:** {c.orgao_nome or 'N/A'}",
                f"**Fornecedor:** {c.fornecedor_nome or 'N/A'} ({c.fornecedor_cnpj or 'N/A'})",
                f"**Contrato nº:** {c.numero_contrato or 'N/A'}",
                f"**Valor:** {valor}",
                f"**Vigência:** {c.vigencia_inicio or 'N/A'} a {c.vigencia_fim or 'N/A'}",
                f"**Situação:** {c.situacao or 'N/A'}",
                "",
            ]
        )

    if texto:
        lines.append(f"*Filtrado localmente por '{texto}'.*")
    if resultado.total > len(resultado.contratos):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)


async def buscar_atas(
    data_inicial: str,
    data_final: str,
    ctx: Context,
    texto: str | None = None,
    cnpj_orgao: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск протоколов регистрации цен в PNCP по периоду действия.

    Примечание: инструмент совместимости для бразильских данных PNCP.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Протоколы регистрации цен — документы, фиксирующие цены, применяемые
    в закупках для будущих приобретений. Поиск фильтруется по периоду
    действия (не по дате публикации).

    ВАЖНО: API PNCP не поддерживает текстовый поиск.
    Параметр 'texto' фильтрует результаты локально.

    Args:
        data_inicial: Начальная дата в формате YYYYMMDD (напр.: 20250101).
            Также принимает YYYY-MM-DD или DD/MM/YYYY.
        data_final: Конечная дата в формате YYYYMMDD (напр.: 20250331).
            Максимум 365 дней между датами.
        texto: Локальный текстовый фильтр (необязательно). Фильтрует по объекту,
            органу или поставщику ПОСЛЕ получения результатов API.
        cnpj_orgao: CNPJ органа-заказчика (необязательно).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных протоколов регистрации цен.
    """
    await ctx.info(f"Buscando atas de registro de preço ({data_inicial} a {data_final})...")

    try:
        resultado = await client.buscar_atas(
            data_inicial=data_inicial,
            data_final=data_final,
            texto=texto,
            cnpj_orgao=cnpj_orgao,
            pagina=pagina,
        )
    except ValueError as e:
        return f"Erro de validação: {e}"

    await ctx.info(f"{resultado.total} atas encontradas")

    if not resultado.atas:
        filtro = f" contendo '{texto}'" if texto else ""
        return (
            f"Nenhuma ata de registro de preço encontrada "
            f"entre {data_inicial} e {data_final}{filtro}."
        )

    lines = [f"**Total:** {resultado.total} atas\n"]
    for i, a in enumerate(resultado.atas, 1):
        valor = format_rub(a.valor_total) if a.valor_total else "N/A"
        lines.extend(
            [
                f"### {i}. {a.objeto or 'Sem descrição'}",
                f"**Órgão:** {a.orgao_nome or 'N/A'}",
                f"**Fornecedor:** {a.fornecedor_nome or 'N/A'} ({a.fornecedor_cnpj or 'N/A'})",
                f"**Ata nº:** {a.numero_ata or 'N/A'}",
                f"**Valor total:** {valor}",
                f"**Vigência:** {a.vigencia_inicio or 'N/A'} a {a.vigencia_fim or 'N/A'}",
                f"**Situação:** {a.situacao or 'N/A'}",
                "",
            ]
        )

    if texto:
        lines.append(f"*Filtrado localmente por '{texto}'.*")
    if resultado.total > len(resultado.atas):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)


async def consultar_fornecedor(cnpj: str, ctx: Context) -> str:
    """(legacy) Запрос информации о поставщике государственных закупок по CNPJ.

    Примечание: инструмент совместимости для бразильских данных PNCP.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает регистрационные данные поставщика в PNCP (Национальный портал
    государственных закупок).

    Args:
        cnpj: CNPJ поставщика (с форматированием или без).

    Returns:
        Данные найденного поставщика.
    """
    await ctx.info(f"Consultando fornecedor CNPJ {cnpj}...")
    resultado = await client.consultar_fornecedor(cnpj=cnpj)
    await ctx.info(f"{resultado.total} fornecedor(es) encontrado(s)")

    if not resultado.fornecedores:
        return f"Nenhum fornecedor encontrado com CNPJ {cnpj}."

    lines: list[str] = []
    for f in resultado.fornecedores:
        lines.extend(
            [
                f"**{f.razao_social or 'N/A'}**",
                f"**CNPJ:** {f.cnpj or 'N/A'}",
                f"**Nome fantasia:** {f.nome_fantasia or 'N/A'}",
                f"**Local:** {f.municipio or 'N/A'}/{f.uf or 'N/A'}",
                f"**Porte:** {f.porte or 'N/A'}",
                f"**Abertura:** {f.data_abertura or 'N/A'}",
                "",
            ]
        )
    return "\n".join(lines)


async def consultar_orgao(
    ctx: Context,
    texto: str | None = None,
    uf: str | None = None,
    pagina: int = 1,
) -> str:
    """(legacy) Поиск органов-заказчиков в PNCP.

    Примечание: инструмент совместимости для бразильских данных PNCP.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Поиск государственных органов, осуществляющих закупки. Полезно для
    обнаружения CNPJ конкретного органа для фильтрации других запросов.

    Args:
        texto: Название органа (частичное или полное).
        uf: Аббревиатура штата органа (напр.: SP, RJ, DF).
        pagina: Страница результатов (по умолчанию 1).

    Returns:
        Список найденных органов.
    """
    if not any([texto, uf]):
        return "Informe pelo menos um filtro: texto ou uf."

    desc = texto or uf or "órgãos"
    await ctx.info(f"Buscando órgãos '{desc}'...")
    resultado = await client.consultar_orgao(query=texto, uf=uf, pagina=pagina)
    await ctx.info(f"{resultado.total} órgãos encontrados")

    if not resultado.orgaos:
        return f"Nenhum órgão encontrado para '{desc}'."

    lines = [f"**Total:** {resultado.total} órgãos\n"]
    for i, o in enumerate(resultado.orgaos, 1):
        lines.extend(
            [
                f"### {i}. {o.razao_social or 'N/A'}",
                f"**CNPJ:** {o.cnpj or 'N/A'}",
                f"**Esfera:** {o.esfera or 'N/A'} | **Poder:** {o.poder or 'N/A'}",
                f"**Local:** {o.municipio or 'N/A'}/{o.uf or 'N/A'}",
                "",
            ]
        )

    if resultado.total > len(resultado.orgaos):
        lines.append(f"*Use pagina={pagina + 1} para mais resultados.*")
    return "\n".join(lines)
