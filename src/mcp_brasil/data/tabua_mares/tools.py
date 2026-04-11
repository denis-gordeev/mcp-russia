"""Tool functions for the Tabua Mares feature.

Инструмент совместимости с API данных о приливах и отливах Бразилии.
Эти инструменты обеспечивают устаревший доступ к бразильским данным
в рамках mcp-russia.

Правила (ADR-001):
    - tools.py НИКОГДА не выполняет HTTP напрямую — делегирует client.py
    - Возвращает отформатированные строки для потребления LLM
    - Использует Context для структурированного логирования и отчёта о прогрессе
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import markdown_table

from . import client
from .constants import ESTADOS_COSTEIROS


async def listar_estados_costeiros(ctx: Context) -> str:
    """(legacy) Список 17 прибрежных штатов Бразилии с портами для запроса данных о приливах.

    Примечание: инструмент совместимости для бразильских данных о приливах.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Используйте этот инструмент для обнаружения штатов с доступными данными о приливах.

    Returns:
        Таблица с аббревиатурой и названием каждого прибрежного штата.
    """
    await ctx.info("Buscando estados costeiros...")
    estados = await client.listar_estados()
    rows = [(sigla.upper(), ESTADOS_COSTEIROS.get(sigla, sigla)) for sigla in estados]
    return markdown_table(["Sigla", "Estado"], rows)


async def listar_portos(estado: str, ctx: Context) -> str:
    """(legacy) Список всех доступных портов в прибрежном штате.

    Примечание: инструмент совместимости для бразильских данных о приливах.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Используйте этот инструмент для обнаружения портов штата перед запросом таблицы приливов.

    Args:
        estado: Аббревиатура штата строчными буквами (напр.: pb, rj, sp, sc).

    Returns:
        Таблица с ID, названием порта и учреждением, собирающим данные.
    """
    await ctx.info(f"Buscando portos de {estado.upper()}...")
    portos = await client.listar_portos_estado(estado)
    rows = [(str(p.id), p.harbor_name, str(p.year), p.data_collection_institution) for p in portos]
    return markdown_table(["ID", "Porto", "Ano", "Instituição"], rows)


async def buscar_portos(ids: list[str], ctx: Context) -> str:
    """(legacy) Поиск подробной информации о конкретных портах по ID.

    Примечание: инструмент совместимости для бразильских данных о приливах.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает данные, включая географическое положение, часовой пояс и средний уровень моря.

    Args:
        ids: Список ID портов (напр.: ['pb01', 'al01', 'rj02']).

    Returns:
        Подробные данные о каждом найденном порте.
    """
    await ctx.info(f"Buscando detalhes dos portos: {', '.join(ids)}...")
    portos = await client.buscar_portos(ids)
    lines: list[str] = []
    for p in portos:
        lines.append(f"## {p.harbor_name}")
        lines.append(f"- **Estado:** {p.state.upper()}")
        lines.append(f"- **Fuso horário:** {p.timezone}")
        lines.append(f"- **Carta náutica:** {p.card}")
        if p.mean_level is not None:
            lines.append(f"- **Nível médio:** {p.mean_level:.2f} m")
        if p.geo_location:
            geo = p.geo_location[0]
            lines.append(f"- **Coordenadas:** {geo.decimal_lat}, {geo.decimal_lng}")
        lines.append("")
    return "\n".join(lines) if lines else "Nenhum porto encontrado."


async def consultar_tabua_mare(
    porto_id: str,
    mes: int,
    dias: str,
    ctx: Context,
) -> str:
    """(legacy) Запрос таблицы приливов порта для конкретных дней месяца.

    Примечание: инструмент совместимости для бразильских данных о приливах.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Возвращает время и уровень прилива и отлива для каждого запрошенного дня.
    Сначала используйте listar_portos для обнаружения ID нужного порта.

    Args:
        porto_id: ID порта (напр.: 'pb01', 'al01').
        mes: Нужный месяц (1-12).
        dias: Дни в формате '1,2,3' или '1,5-13' (конкретные дни и/или интервалы).

    Returns:
        Форматированная таблица приливов со временем и уровнями.
    """
    await ctx.info(f"Consultando tábua de marés do porto {porto_id}, mês {mes}...")
    tabuas = await client.consultar_tabua_mare(porto_id, mes, dias)
    if not tabuas:
        return "Nenhum dado de maré encontrado para os parâmetros informados."

    lines: list[str] = []
    for tabua in tabuas:
        lines.append(f"## {tabua.harbor_name} ({tabua.state.upper()})")
        lines.append(
            f"Ano: {tabua.year} | Fuso: {tabua.timezone} | Nível médio: {tabua.mean_level:.2f} m"
        )
        lines.append("")
        for mes_data in tabua.months:
            lines.append(f"### {mes_data.month_name}")
            for dia in mes_data.days:
                lines.append(f"\n**{dia.weekday_name.capitalize()}, dia {dia.day}:**")
                rows = [(h.hour, f"{h.level:.2f} m") for h in dia.hours]
                lines.append(markdown_table(["Horário", "Nível"], rows))
    return "\n".join(lines)


async def porto_mais_proximo(
    estado: str,
    lat: float,
    lng: float,
    ctx: Context,
) -> str:
    """(legacy) Поиск ближайшего порта к координате в пределах штата.

    Примечание: инструмент совместимости для бразильских данных о приливах.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Используйте этот инструмент, если известен штат и координаты пользователя.

    Args:
        estado: Аббревиатура штата (напр.: pb, rj, sp).
        lat: Широта (напр.: -7.11509).
        lng: Долгота (напр.: -34.864).

    Returns:
        Данные ближайшего порта.
    """
    await ctx.info(f"Buscando porto mais próximo em {estado.upper()}...")
    portos = await client.porto_mais_proximo(estado, lat, lng)
    if not portos:
        return "Nenhum porto encontrado próximo às coordenadas informadas."
    p = portos[0]
    lines = [
        f"## {p.harbor_name}",
        f"- **Estado:** {p.state.upper()}",
        f"- **Fuso horário:** {p.timezone}",
        f"- **Carta náutica:** {p.card}",
    ]
    if p.mean_level is not None:
        lines.append(f"- **Nível médio:** {p.mean_level:.2f} m")
    if p.geo_location:
        geo = p.geo_location[0]
        lines.append(f"- **Coordenadas:** {geo.decimal_lat}, {geo.decimal_lng}")
    return "\n".join(lines)


async def porto_mais_proximo_geral(lat: float, lng: float, ctx: Context) -> str:
    """(legacy) Поиск ближайшего порта к координате независимо от штата.

    Примечание: инструмент совместимости для бразильских данных о приливах.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Используйте этот инструмент, если неизвестен штат пользователя, только координаты.

    Args:
        lat: Широта (напр.: -7.11509).
        lng: Долгота (напр.: -34.864).

    Returns:
        Данные ближайшего порта.
    """
    await ctx.info("Buscando porto mais próximo (qualquer estado)...")
    portos = await client.porto_mais_proximo_geral(lat, lng)
    if not portos:
        return "Nenhum porto encontrado próximo às coordenadas informadas."
    p = portos[0]
    lines = [
        f"## {p.harbor_name}",
        f"- **Estado:** {p.state.upper()}",
        f"- **Fuso horário:** {p.timezone}",
        f"- **Carta náutica:** {p.card}",
    ]
    if p.mean_level is not None:
        lines.append(f"- **Nível médio:** {p.mean_level:.2f} m")
    if p.geo_location:
        geo = p.geo_location[0]
        lines.append(f"- **Coordenadas:** {geo.decimal_lat}, {geo.decimal_lng}")
    return "\n".join(lines)


async def tabua_mare_por_geolocalizacao(
    lat: float,
    lng: float,
    estado: str,
    mes: int,
    dias: str,
    ctx: Context,
) -> str:
    """(legacy) Получение таблицы приливов ближайшего порта по географическим координатам.

    Примечание: инструмент совместимости для бразильских данных о приливах.
    Эти инструменты обеспечивают устаревший доступ к бразильским данным
    в рамках mcp-russia.
    Комбинирует поиск ближайшего порта с запросом таблицы приливов
    в одном вызове. Идеально, когда пользователь сообщает своё местоположение.

    Args:
        lat: Широта (напр.: -7.11509).
        lng: Долгота (напр.: -34.864).
        estado: Аббревиатура штата (напр.: pb, rj, sp).
        mes: Нужный месяц (1-12).
        dias: Дни в формате '1,2,3' или '1,5-13' (конкретные дни и/или интервалы).

    Returns:
        Таблица приливов ближайшего порта.
    """
    await ctx.info(f"Consultando marés por geolocalização ({lat}, {lng})...")
    tabuas = await client.tabua_mare_por_geolocalizacao(lat, lng, estado, mes, dias)
    if not tabuas:
        return "Nenhum dado de maré encontrado para as coordenadas informadas."

    lines: list[str] = []
    for tabua in tabuas:
        lines.append(f"## {tabua.harbor_name} ({tabua.state.upper()})")
        lines.append(
            f"Ano: {tabua.year} | Fuso: {tabua.timezone} | Nível médio: {tabua.mean_level:.2f} m"
        )
        lines.append("")
        for mes_data in tabua.months:
            lines.append(f"### {mes_data.month_name}")
            for dia in mes_data.days:
                lines.append(f"\n**{dia.weekday_name.capitalize()}, dia {dia.day}:**")
                rows = [(h.hour, f"{h.level:.2f} m") for h in dia.hours]
                lines.append(markdown_table(["Horário", "Nível"], rows))
    return "\n".join(lines)
