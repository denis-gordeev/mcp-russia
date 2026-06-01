"""Tool functions for the Росгидромет feature.

Tools for accessing weather, climate, environmental, and satellite monitoring data.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_number_ru, markdown_table

from . import client


async def spisok_stanciy(ctx: Context) -> str:
    """Получить список станций мониторинга Росгидромета.

    Returns:
        Список станций с кодами.
    """
    await ctx.info("Запрос списка станций мониторинга...")
    stancii = client.get_stancii_list()

    rows = [(s["code"], s["name"], s["region"]) for s in stancii]
    header = "**Станции мониторинга Росгидромета**\n\n"
    return header + markdown_table(["Код", "Город", "Округ"], rows)


async def spisok_tipov_dannykh(ctx: Context) -> str:
    """Получить список типов метеорологических и экологических данных.

    Returns:
        Список типов данных.
    """
    await ctx.info("Запрос списка типов данных...")
    meteo = client.get_tipy_meteo_list()
    eko = client.get_tipy_eko_list()

    lines = ["**Типы метеорологических данных**\n"]
    rows = [(m["code"], m["name"]) for m in meteo]
    lines.append(markdown_table(["Код", "Тип"], rows))

    lines.append("\n**Типы экологических данных**\n")
    rows = [(e["code"], e["name"]) for e in eko]
    lines.append(markdown_table(["Код", "Тип"], rows))

    return "\n".join(lines)


async def pogoda_seychas(stanciya: str = "77", ctx: Context | None = None) -> str:
    """Получить текущую погоду на станции.

    Args:
        stanciya: Код станции (по умолчанию Москва — 77).

    Returns:
        Текущие погодные данные.
    """
    await ctx.info(f"Запрос текущей погоды на станции {stanciya}...")
    data = await client.poluchit_pogodu(stanciya)

    if not data:
        return (
            f"Данные о погоде для станции '{stanciya}' недоступны.\n\n"
            f"Используйте spisok_stanciy() для списка станций."
        )

    lines = [f"**Погода: {data.gorod}** ({data.region})"]
    if data.temperatura:
        lines.append(f"- Температура: {format_number_ru(data.temperatura, 1)}°C")
    if data.feels_like:
        lines.append(f"- Ощущается как: {format_number_ru(data.feels_like, 1)}°C")
    if data.vlazhnost:
        lines.append(f"- Влажность: {format_number_ru(data.vlazhnost, 0)}%")
    if data.davlenie:
        lines.append(f"- Давление: {format_number_ru(data.davlenie, 0)} мм рт.ст.")
    if data.veter_skorost:
        lines.append(
            f"- Ветер: {format_number_ru(data.veter_skorost, 1)} м/с {data.veter_napravlenie}"
        )
    if data.osadki is not None:
        lines.append(f"- Осадки: {format_number_ru(data.osadki, 1)} мм")
    if data.opisaniye:
        lines.append(f"- Описание: {data.opisaniye}")
    if data.data_vremya:
        lines.append(f"- Данные на: {data.data_vremya}")
    lines.append("- Источник: Open-Meteo / Росгидромет")
    return "\n".join(lines)


async def prognoz_pogody(
    stanciya: str = "77",
    dni: int = 3,
    ctx: Context | None = None,
) -> str:
    """Получить прогноз погоды на несколько дней.

    Args:
        stanciya: Код станции.
        dni: Количество дней прогноза (1-7).

    Returns:
        Прогноз погоды.
    """
    await ctx.info(f"Запрос прогноза на {dni} дней для станции {stanciya}...")
    prognoz = await client.poluchit_prognoz(stanciya, dni)

    if not prognoz:
        return (
            f"Прогноз погоды для станции '{stanciya}' недоступен.\n\n"
            f"Используйте spisok_stanciy() для списка станций."
        )

    lines = [f"**Прогноз погоды** — {len(prognoz)} дней\n"]
    for p in prognoz:
        lines.append(f"**{p.data}**")
        if p.temperatura_dnem is not None:
            lines.append(f"- Днём: {format_number_ru(p.temperatura_dnem, 1)}°C")
        if p.temperatura_nochyu is not None:
            lines.append(f"- Ночью: {format_number_ru(p.temperatura_nochyu, 1)}°C")
        if p.osadki_veroyatnost is not None:
            lines.append(f"- Осадки: {format_number_ru(p.osadki_veroyatnost, 0)}%")
        if p.opisaniye:
            lines.append(f"- {p.opisaniye}")
        lines.append("")

    lines.append("- Источник: Open-Meteo / Росгидромет")
    return "\n".join(lines)


async def ekologiya_regiona(
    gorod: str = "",
    tip: str = "",
    ctx: Context | None = None,
) -> str:
    """Получить данные об экологической обстановке.

    Args:
        gorod: Название города (необязательно).
        tip: Тип данных (vozdukh, voda, pochva, radiaciya, shum).

    Returns:
        Данные об экологической обстановке.
    """
    await ctx.info(f"Запрос экологических данных: город={gorod}, тип={tip}")
    data = await client.poluchit_ekologiyu(gorod=gorod, tip=tip)

    if not data:
        filters = []
        if gorod:
            filters.append(f"город: {gorod}")
        if tip:
            filters.append(f"тип: {tip}")
        filter_text = f" ({', '.join(filters)})" if filters else ""
        return (
            f"Экологические данные{filter_text} недоступны.\n\n"
            f"Данные доступны на сайте Росприроднадзора: rpn.gov.ru"
        )

    lines = [f"**Экологическая обстановка** — измерений: {len(data)}\n"]
    for d in data[:10]:
        line = f"- {d.gorod} ({d.tip}): {d.pokazatel}"
        if d.znachenie is not None:
            line += f" = {format_number_ru(d.znachenie, 2)}"
        if d.prevyshenie:
            line += " ⚠️ ПРЕВЫШЕНИЕ нормы"
        lines.append(line)

    if len(data) > 10:
        lines.append(f"\n... и ещё {len(data) - 10} измерений")

    lines.append("- Источник: Open-Meteo Air Quality")
    return "\n".join(lines)


async def preduprezhdeniya(region: str = "", ctx: Context | None = None) -> str:
    """Получить активные предупреждения об опасных явлении.

    Args:
        region: Регион (необязательно).

    Returns:
        Активные предупреждения.
    """
    await ctx.info(f"Запрос предупреждений для региона {region}...")
    data = await client.poluchit_preduprezhdeniya(region)

    if not data:
        region_text = f" для региона '{region}'" if region else ""
        return (
            f"Активные предупреждения{region_text} отсутствуют.\n\n"
            f"Метеорологические данные: open-meteo.com / meteorf.ru"
        )

    lines = [f"**Активные предупреждения** — {len(data)}\n"]
    for p in data:
        lines.append(f"⚠️ **{p.tip}** — {p.region}, {p.gorod}")
        lines.append(f"   {p.opisanie}")
        if p.data_nachala:
            lines.append(f"   С: {p.data_nachala}")
        if p.data_okonchaniya:
            lines.append(f"   По: {p.data_okonchaniya}")
        lines.append(f"   Уровень опасности: {p.uroven_opasnosti}")
        lines.append("")

    lines.append("- Источник: Open-Meteo / Росгидромет")
    return "\n".join(lines)


async def sputnik_monitoring(
    region: str = "",
    tip: str = "",
    ctx: Context | None = None,
) -> str:
    """Получить данные спутникового мониторинга.

    Args:
        region: Регион (необязательно).
        tip: Тип данных (lesa, voda, pozhary, snezhnyy_pokrov).

    Returns:
        Данные спутникового мониторинга.
    """
    await ctx.info(f"Запрос спутниковых данных: регион={region}, тип={tip}")
    data = await client.poluchit_sputnik_dannye(region, tip)

    if not data:
        filters = []
        if region:
            filters.append(f"регион: {region}")
        if tip:
            filters.append(f"тип: {tip}")
        filter_text = f" ({', '.join(filters)})" if filters else ""
        return (
            f"Данные спутникового мониторинга{filter_text} недоступны.\n\n"
            f"Спутниковые данные: niikp-atm.ru"
        )

    lines = [f"**Спутниковый мониторинг** — снимков: {len(data)}\n"]
    for s in data[:5]:
        lines.append(f"- {s.region} ({s.data_syomki}): {s.tip_dannykh}")
        lines.append(f"  Спутник: {s.sputnik}, Разрешение: {s.razreshenie}")
        if s.izobrazhenie_url:
            lines.append(f"  Изображение: {s.izobrazhenie_url}")
        lines.append("")

    if len(data) > 5:
        lines.append(f"\n... и ещё {len(data) - 5} снимков")

    lines.append("- Источник: Росгидромет / НИИ КП")
    return "\n".join(lines)
