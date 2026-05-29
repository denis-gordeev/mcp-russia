"""Tool functions for the Saúde feature.

Инструмент совместимости с API данных здравоохранения Бразилии (CNES/DataSUS).
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_number_ru, markdown_table

from . import client


async def buscar_estabelecimentos(
    ctx: Context,
    codigo_municipio: str | None = None,
    codigo_uf: str | None = None,
    status: int | None = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """(legacy) Поиск учреждений здравоохранения, зарегистрированных в CNES/DataSUS.

    Примечание: инструмент совместимости для бразильских данных здравоохранения.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Запрос в Национальный реестр учреждений здравоохранения для поиска
    больниц, UBS, клиник и других учреждений. Фильтруйте по муниципалитету
    или штату для более релевантных результатов.

    Args:
        codigo_municipio: Код IBGE муниципалитета (напр.: "355030" для Сан-Паулу).
        codigo_uf: Код IBGE штата (напр.: "35" для SP, "33" для RJ).
        status: 1 — активные, 0 — неактивные. Если пропущено, возвращает все.
        limit: Максимальное количество результатов (по умолчанию: 20, максимум: 100).
        offset: Смещение для пагинации (по умолчанию: 0).

    Returns:
        Таблица с найденными учреждениями.
    """
    filtro = codigo_municipio or codigo_uf or "Brasil"
    await ctx.info(f"Buscando estabelecimentos de saúde em {filtro}...")

    resultados = await client.buscar_estabelecimentos(
        codigo_municipio=codigo_municipio,
        codigo_uf=codigo_uf,
        status=status,
        limit=limit,
        offset=offset,
    )

    if not resultados:
        return "Nenhum estabelecimento encontrado para os filtros informados."

    rows = [
        (
            e.codigo_cnes or "—",
            e.nome_fantasia or e.nome_razao_social or "—",
            e.descricao_tipo or "—",
            e.tipo_gestao or "—",
            e.endereco or "—",
        )
        for e in resultados
    ]

    header = f"**Estabelecimentos de saúde** ({len(resultados)} resultados)\n\n"
    return header + markdown_table(["CNES", "Nome", "Tipo", "Gestão", "Endereço"], rows)


async def buscar_profissionais(
    ctx: Context,
    codigo_municipio: str | None = None,
    cnes: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """(legacy) Поиск специалистов здравоохранения, зарегистрированных в CNES/DataSUS.

    Примечание: инструмент совместимости для бразильских данных здравоохранения.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Запрос специалистов, привязанных к учреждениям здравоохранения.
    Фильтруйте по муниципалитету или коду CNES учреждения.

    Args:
        codigo_municipio: Код IBGE муниципалитета (напр.: "355030").
        cnes: Код CNES учреждения (напр.: "1234567").
        limit: Максимальное количество результатов (по умолчанию: 20, максимум: 100).
        offset: Смещение для пагинации (по умолчанию: 0).

    Returns:
        Таблица с найденными специалистами.
    """
    filtro = cnes or codigo_municipio or "Brasil"
    await ctx.info(f"Buscando profissionais de saúde em {filtro}...")

    resultados = await client.buscar_profissionais(
        codigo_municipio=codigo_municipio,
        cnes=cnes,
        limit=limit,
        offset=offset,
    )

    if not resultados:
        return "Nenhum profissional encontrado para os filtros informados."

    rows = [
        (
            p.codigo_cnes or "—",
            p.nome or "—",
            p.cbo or "—",
            p.descricao_cbo or "—",
        )
        for p in resultados
    ]

    header = f"**Profissionais de saúde** ({len(resultados)} resultados)\n\n"
    return header + markdown_table(["CNES", "Nome", "CBO", "Ocupação"], rows)


async def listar_tipos_estabelecimento(ctx: Context) -> str:
    """(legacy) Список всех типов учреждений здравоохранения CNES.

    Примечание: инструмент совместимости для бразильских данных здравоохранения.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает таблицу типов (код и описание), используемых для классификации
    учреждений здравоохранения SUS, таких как больницы, UBS, CAPS и т.д.

    Returns:
        Таблица со всеми типами учреждений.
    """
    await ctx.info("Listando tipos de estabelecimento de saúde...")

    resultados = await client.listar_tipos_estabelecimento()

    if not resultados:
        return "Nenhum tipo de estabelecimento encontrado."

    rows = [(t.codigo or "—", t.descricao or "—") for t in resultados]

    header = f"**Tipos de estabelecimento de saúde** ({len(resultados)} tipos)\n\n"
    return header + markdown_table(["Código", "Descrição"], rows)


async def consultar_leitos(
    ctx: Context,
    codigo_municipio: str | None = None,
    cnes: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> str:
    """(legacy) Запрос данных о больничных койках, зарегистрированных в CNES/DataSUS.

    Примечание: инструмент совместимости для бразильских данных здравоохранения.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает данные о существующих койках и койках SUS по учреждениям,
    включая тип койки и специализацию. Полезно для анализа больничной
    мощности региона.

    Args:
        codigo_municipio: Код IBGE муниципалитета (напр.: "355030").
        cnes: Код CNES учреждения (напр.: "1234567").
        limit: Максимальное количество результатов (по умолчанию: 20, максимум: 100).
        offset: Смещение для пагинации (по умолчанию: 0).

    Returns:
        Таблица с найденными больничными койками.
    """
    filtro = cnes or codigo_municipio or "Brasil"
    await ctx.info(f"Consultando leitos hospitalares em {filtro}...")

    resultados = await client.consultar_leitos(
        codigo_municipio=codigo_municipio,
        cnes=cnes,
        limit=limit,
        offset=offset,
    )

    if not resultados:
        return "Nenhum leito encontrado para os filtros informados."

    total_existente = sum(leito.existente or 0 for leito in resultados)
    total_sus = sum(leito.sus or 0 for leito in resultados)

    rows = [
        (
            leito.codigo_cnes or "—",
            leito.tipo_leito or "—",
            leito.especialidade or "—",
            format_number_ru(float(leito.existente), 0) if leito.existente is not None else "—",
            format_number_ru(float(leito.sus), 0) if leito.sus is not None else "—",
        )
        for leito in resultados
    ]

    header = (
        f"**Leitos hospitalares** ({len(resultados)} registros)\n"
        f"Total existentes: {format_number_ru(float(total_existente), 0)} | "
        f"Total SUS: {format_number_ru(float(total_sus), 0)}\n\n"
    )
    return header + markdown_table(["CNES", "Tipo", "Especialidade", "Existentes", "SUS"], rows)
