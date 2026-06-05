"""Tool functions for the Rosstat feature.

Tools for accessing Rosstat demographic, economic, and regional data.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_number_ru, markdown_table

from . import client
from .constants import KLYUCHEVYE_INDIKATORY


async def spisok_regionov(ctx: Context) -> str:
    """Получить список субъектов Российской Федерации.

    Returns:
        Список субъектов РФ с кодами.
    """
    await ctx.info("Запрос списка субъектов РФ...")
    regiony = client.get_subiekty_list()

    rows = [(r["code"], r["name"], r.get("okrug", "")) for r in regiony]
    header = f"**Субъекты Российской Федерации** — {len(regiony)} субъектов\n\n"
    return header + markdown_table(["Код", "Регион", "ФО"], rows)


async def spisok_okrugov(ctx: Context) -> str:
    """Получить список федеральных округов РФ.

    Returns:
        Список федеральных округов.
    """
    await ctx.info("Запрос списка федеральных округов...")
    okruga = client.get_federalny_okruga_list()

    rows = [(o["code"], o["name"]) for o in okruga]
    header = "**Федеральные округа Российской Федерации**\n\n"
    return header + markdown_table(["Код", "Округ"], rows)


async def region_info(kod: str, ctx: Context) -> str:
    """Получить информацию о субъекте РФ по коду.

    Args:
        kod: Код региона (OKATO).

    Returns:
        Информация о регионе.
    """
    await ctx.info(f"Запрос информации о регионе {kod}...")
    data = await client.poluchit_dannye_regiona(kod)

    if not data:
        return (
            f"Регион с кодом '{kod}' не найден.\n\n"
            f"Используйте spisok_regionov() для списка субъектов."
        )

    lines = [
        f"**{data.name}** (код {data.code})",
    ]
    if data.federalny_okrug:
        lines.append(f"- Федеральный округ: {data.federalny_okrug}")
    if data.population:
        lines.append(f"- Население: {format_number_ru(data.population, 0)} чел.")
    if data.vrp:
        lines.append(f"- ВРП: {format_number_ru(data.vrp, 2)} млрд ₽")
    if data.srednyaya_zp:
        lines.append(f"- Средняя зарплата: {format_number_ru(data.srednyaya_zp, 2)} ₽")

    lines.append("- Источник: Росстат / ЕМИСС (fedstat.ru)")
    return "\n".join(lines)


async def okrug_info(kod: str, ctx: Context) -> str:
    """Получить информацию о федеральном округе.

    Args:
        kod: Код федерального округа.

    Returns:
        Информация о федеральном округе.
    """
    await ctx.info(f"Запрос информации о федеральном округе {kod}...")
    data = await client.poluchit_federalny_okrug(kod)

    if "error" in data:
        return f"{data['error']}\n\nИспользуйте spisok_okrugov() для списка округов."

    lines = [
        f"**{data['name']}** (код {data['code']})",
        f"- Субъектов в округе: {data.get('kolichestvo_subiektov', 0)}",
    ]
    subiekty = data.get("subiekty", [])
    if subiekty:
        lines.append(f"- Субъекты: {', '.join(subiekty[:5])}")
        if len(subiekty) > 5:
            lines.append(f"  и ещё {len(subiekty) - 5} субъектов")

    return "\n".join(lines)


async def pokazateli_rosstata(ctx: Context) -> str:
    """Получить список основных показателей Росстата.

    Returns:
        Список доступных показателей.
    """
    await ctx.info("Запрос списка показателей Росстата...")

    rows = [(p["code"], p["name"]) for p in KLYUCHEVYE_INDIKATORY]
    header = "**Основные показатели Росстата**\n\n"
    return header + markdown_table(["Код", "Показатель"], rows)


async def inflyaciya(god: str = "", ctx: Context | None = None) -> str:
    """Получить данные об инфляции (ИПЦ) в России.

    Args:
        god: Год для запроса (например, '2025'). По умолчанию — текущий.

    Returns:
        Данные об инфляции.
    """
    if ctx:
        await ctx.info("Запрос данных об инфляции...")
    data = await client.poluchit_inflyaciyu(god)
    if not data:
        return (
            f"**Инфляция в России (ИПЦ)**\n\n"
            f"Данные об индексе потребительских цен доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/31088\n"
            f"- Росстат: https://rosstat.gov.ru/statistics/price\n\n"
            f"Для запроса данных за {god or 'текущий период'} "
            f"используйте показатель 'cpi' через API ЕМИСС."
        )
    rows = []
    for d in data:
        ipcz_m = f"{d.get('ipcz_mesyac', '')}%" if d.get("ipcz_mesyac") else "—"
        ipcz_n = f"{d.get('ipcz_nakoplenny', '')}%" if d.get("ipcz_nakoplenny") else "—"
        ipcz_g = f"{d.get('ipcz_god', '')}%" if d.get("ipcz_god") else "—"
        rows.append((d.get("period", ""), ipcz_m, ipcz_n, ipcz_g))
    header = "**Инфляция в России (ИПЦ)**\n\n"
    header += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return header + markdown_table(
        ["Период", "К мес.", "Накопл.", "К г/г"],
        rows,
    )


async def demografiya(region: str = "", ctx: Context | None = None) -> str:
    """Получить демографические данные по России или региону.

    Args:
        region: Код региона (необязательно).

    Returns:
        Демографические данные.
    """
    if ctx:
        await ctx.info("Запрос демографических данных...")
    data = await client.poluchit_demografiyu(region)
    filter_text = f" по региону {region}" if region else " по России"
    if not data:
        return (
            f"**Демографические данные{filter_text}**\n\n"
            f"Демографическая статистика (рождаемость, смертность, "
            f"численность населения) доступна через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/24133\n"
            f"- Росстат: https://rosstat.gov.ru/statistics/population\n\n"
            f"Для получения конкретных данных используйте API ЕМИСС."
        )
    rows = []
    for d in data:
        nas = format_number_ru(d["naselenie"], 0) if d.get("naselenie") else "—"
        rozh = f"{d.get('rozhdaemost', '')}‰" if d.get("rozhdaemost") else "—"
        sm = f"{d.get('smertnost', '')}‰" if d.get("smertnost") else "—"
        rows.append((d.get("period", ""), nas, rozh, sm))
    header = f"**Демографические данные{filter_text}**\n\n"
    header += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return header + markdown_table(
        ["Период", "Население", "Рожд.", "Смерт."],
        rows,
    )
