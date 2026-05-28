"""Инструменты для работы с INPE (Национальный институт космических исследований, legacy).

Примечание: это слой совместимости в рамках mcp-russia. Данные инструменты
предоставляют устаревший доступ к данным бразильского INPE (мониторинг
лесных пожаров и вырубок) и считаются переходными.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_number_ru, markdown_table

from . import client
from .constants import BIOMAS, DEFAULT_LIMIT


async def buscar_focos_queimadas(
    ctx: Context,
    estado: str | None = None,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    satelite: str | None = None,
    limite: int = DEFAULT_LIMIT,
) -> str:
    """(legacy) Поиск очагов лесных пожаров, обнаруженных спутниками в Бразилии.

    Инструмент совместимости с INPE (Бразилия). Данные BD Queimadas.
    Возвращает информацию об обнаруженных пожарах: координаты, спутник,
    биом и уровень риска.

    Args:
        estado: Аббревиатура штата из 2 букв (напр.: PA, MT, AM). Необязательно.
        data_inicio: Дата начала в формате YYYY-MM-DD. Необязательно.
        data_fim: Дата окончания в формате YYYY-MM-DD. Необязательно.
        satelite: Название спутника (напр.: AQUA_M-T, NPP-375). Необязательно.
        limite: Максимальное количество результатов (по умолчанию: 50).

    Returns:
        Таблица с найденными очагами пожаров.
    """
    filtros = []
    if estado:
        filtros.append(f"estado={estado.upper()}")
    if data_inicio:
        filtros.append(f"de {data_inicio}")
    if data_fim:
        filtros.append(f"até {data_fim}")
    if satelite:
        filtros.append(f"satélite={satelite}")

    filtro_str = f" ({', '.join(filtros)})" if filtros else ""
    await ctx.info(f"Buscando focos de queimadas{filtro_str}...")

    focos = await client.buscar_focos(
        estado=estado,
        data_inicio=data_inicio,
        data_fim=data_fim,
        satelite=satelite,
        limite=limite,
    )

    if not focos:
        return "Nenhum foco de queimada encontrado para os filtros informados."

    await ctx.info(f"{len(focos)} focos encontrados")

    rows = [
        (
            f.municipio,
            f.estado,
            f.bioma,
            f"{f.latitude:.4f}",
            f"{f.longitude:.4f}",
            f.satelite,
            f.data_hora,
            format_number_ru(f.risco_fogo, 2) if f.risco_fogo is not None else "—",
        )
        for f in focos
    ]

    header = f"**Focos de queimadas** ({len(focos)} resultados{filtro_str}):\n\n"
    table = markdown_table(
        ["Município", "UF", "Bioma", "Lat", "Lon", "Satélite", "Data/Hora", "Risco"],
        rows,
    )
    return header + table


async def consultar_desmatamento(
    ctx: Context,
    bioma: str | None = None,
    estado: str | None = None,
    ano: int | None = None,
) -> str:
    """(legacy) Запрос исторических данных о вырубке леса PRODES/INPE.

    Инструмент совместимости с INPE (Бразилия).
    PRODES мониторит сплошные вырубки в Legal Amazon и других биомах с 1988 года.
    Консолидированные ежегодные данные.

    Доступные биомы: amazonia, cerrado, mata_atlantica, caatinga, pampa, pantanal.

    Args:
        bioma: Название биома (напр.: amazonia, cerrado). Необязательно.
        estado: Аббревиатура штата из 2 букв (напр.: PA, MT). Необязательно.
        ano: Год (напр.: 2023). Необязательно.

    Returns:
        Таблица с данными о вырубке леса.
    """
    bioma_nome = BIOMAS.get(bioma, bioma) if bioma else None

    filtros = []
    if bioma_nome:
        filtros.append(f"bioma={bioma_nome}")
    if estado:
        filtros.append(f"estado={estado.upper()}")
    if ano:
        filtros.append(f"ano={ano}")

    filtro_str = f" ({', '.join(filtros)})" if filtros else ""
    await ctx.info(f"Consultando desmatamento PRODES{filtro_str}...")

    dados = await client.buscar_dados_prodes(
        bioma=bioma_nome,
        estado=estado,
        ano=ano,
    )

    if not dados:
        return "Nenhum dado de desmatamento encontrado para os filtros informados."

    await ctx.info(f"{len(dados)} registros encontrados")

    rows = [
        (
            str(d.ano),
            d.bioma,
            d.estado,
            d.municipio,
            format_number_ru(d.area_km2, 2),
        )
        for d in dados
    ]

    header = f"**Desmatamento PRODES** ({len(dados)} registros{filtro_str}):\n\n"
    table = markdown_table(["Ano", "Bioma", "UF", "Município", "Área (km²)"], rows)
    return header + table


async def alertas_deter(
    ctx: Context,
    bioma: str | None = None,
    estado: str | None = None,
    data_inicio: str | None = None,
    data_fim: str | None = None,
) -> str:
    """(legacy) Запрос предупреждений о вырубке леса системы DETER/INPE.

    Инструмент совместимости с INPE (Бразилия).
    DETER (Детекция вырубки в реальном времени) выдаёт ежедневные предупреждения
    о вырубке и деградации лесов с использованием спутниковых снимков.

    Доступные биомы: amazonia, cerrado, mata_atlantica, caatinga, pampa, pantanal.

    Args:
        bioma: Название биома (напр.: amazonia, cerrado). Необязательно.
        estado: Аббревиатура штата из 2 букв (напр.: PA, MT). Необязательно.
        data_inicio: Дата начала в формате YYYY-MM-DD. Необязательно.
        data_fim: Дата окончания в формате YYYY-MM-DD. Необязательно.

    Returns:
        Таблица с предупреждениями о вырубке.
    """
    bioma_nome = BIOMAS.get(bioma, bioma) if bioma else None

    filtros = []
    if bioma_nome:
        filtros.append(f"bioma={bioma_nome}")
    if estado:
        filtros.append(f"estado={estado.upper()}")
    if data_inicio:
        filtros.append(f"de {data_inicio}")
    if data_fim:
        filtros.append(f"até {data_fim}")

    filtro_str = f" ({', '.join(filtros)})" if filtros else ""
    await ctx.info(f"Consultando alertas DETER{filtro_str}...")

    alertas = await client.buscar_alertas_deter(
        bioma=bioma_nome,
        estado=estado,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )

    if not alertas:
        return "Nenhum alerta DETER encontrado para os filtros informados."

    await ctx.info(f"{len(alertas)} alertas encontrados")

    rows = [
        (
            a.data,
            a.municipio,
            a.estado,
            a.bioma,
            a.classe,
            format_number_ru(a.area_km2, 2),
            a.satelite,
        )
        for a in alertas
    ]

    header = f"**Alertas DETER** ({len(alertas)} alertas{filtro_str}):\n\n"
    table = markdown_table(
        ["Data", "Município", "UF", "Bioma", "Classe", "Área (km²)", "Satélite"],
        rows,
    )
    return header + table


async def dados_satelite(ctx: Context) -> str:
    """(legacy) Список спутников, доступных для экологического мониторинга INPE.

    Инструмент совместимости с INPE (Бразилия).
    Возвращает спутники, используемые INPE для обнаружения пожаров
    и вырубки леса, включая спутники NASA, NOAA и INPE/CBERS.

    Returns:
        Таблица с доступными спутниками.
    """
    await ctx.info("Listando satélites disponíveis...")
    satelites = await client.listar_satelites()

    if not satelites:
        return "Nenhum satélite disponível no momento."

    await ctx.info(f"{len(satelites)} satélites encontrados")

    rows = [(s.nome, s.descricao) for s in satelites]
    header = f"**Satélites de monitoramento** ({len(satelites)} disponíveis):\n\n"
    table = markdown_table(["Satélite", "Descrição"], rows)
    return header + table
