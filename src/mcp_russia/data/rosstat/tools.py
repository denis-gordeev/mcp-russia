"""Инструменты модуля Росстата.

Инструменты для доступа к демографическим, экономическим и региональным данным Росстата.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client
from .constants import (
    EMISS_KODY_POKAZATELEY,
    KLYUCHEVYE_INDIKATORY,
    OTRASLEVAYA_STRUKTURA_VRP,
    REGIONALNYE_POKAZATELI,
    VIDY_DEYATELNOSTI_INVESTITSII,
)


async def spisok_regionov(ctx: Context) -> str:
    """Получить список субъектов Российской Федерации.

    Возвращает:
        Список субъектов РФ с кодами.
    """
    await ctx.info("Запрос списка субъектов РФ...")
    regiony = client.poluchit_spisok_subiektov()

    stroki_tablitsy = [(r["kod"], r["nazvanie"], r.get("okrug", "")) for r in regiony]
    header = f"**Субъекты Российской Федерации** — {len(regiony)} субъектов\n\n"
    return header + tablitsa_v_markdown(["Код", "Регион", "ФО"], stroki_tablitsy)


async def spisok_okrugov(ctx: Context) -> str:
    """Получить список федеральных округов РФ.

    Возвращает:
        Список федеральных округов.
    """
    await ctx.info("Запрос списка федеральных округов...")
    okruga = client.poluchit_spisok_federalnykh_okrugov()

    stroki_tablitsy = [(o["kod"], o["nazvanie"]) for o in okruga]
    header = "**Федеральные округа Российской Федерации**\n\n"
    return header + tablitsa_v_markdown(["Код", "Округ"], stroki_tablitsy)


async def informatsiya_o_regionye(kod: str, ctx: Context) -> str:
    """Получить информацию о субъекте РФ по коду.

    Аргументы:
        kod: Код региона (OKATO).

    Возвращает:
        Информация о регионе.
    """
    await ctx.info(f"Запрос информации о регионе {kod}...")
    data = await client.poluchit_dannye_regiona(kod)

    if not data:
        return (
            f"Регион с кодом '{kod}' не найден.\n\n"
            f"Используйте spisok_regionov() для списка субъектов."
        )

    stroki = [
        f"**{data.nazvanie}** (код {data.kod})",
    ]
    if data.federalny_okrug:
        stroki.append(f"- Федеральный округ: {data.federalny_okrug}")
    if data.naselenie:
        stroki.append(f"- Население: {formatirovat_chislo_ru(data.naselenie, 0)} чел.")
    if data.vrp:
        stroki.append(f"- ВРП: {formatirovat_chislo_ru(data.vrp, 2)} млрд ₽")
    if data.srednyaya_zp:
        stroki.append(f"- Средняя зарплата: {formatirovat_chislo_ru(data.srednyaya_zp, 2)} ₽")

    stroki.append("- Источник: Росстат / ЕМИСС (fedstat.ru)")
    return "\n".join(stroki)


async def informatsiya_ob_okruge(kod: str, ctx: Context) -> str:
    """Получить информацию о федеральном округе.

    Аргументы:
        kod: Код федерального округа.

    Возвращает:
        Информация о федеральном округе.
    """
    await ctx.info(f"Запрос информации о федеральном округе {kod}...")
    data = await client.poluchit_federalny_okrug(kod)

    if "oshibka" in data:
        return f"{data['oshibka']}\n\nИспользуйте spisok_okrugov() для списка округов."

    stroki = [
        f"**{data['nazvanie']}** (код {data['kod']})",
        f"- Субъектов в округе: {data.get('kolichestvo_subiektov', 0)}",
    ]
    subiekty = data.get("subiekty", [])
    if subiekty:
        stroki.append(f"- Субъекты: {', '.join(subiekty[:5])}")
        if len(subiekty) > 5:
            stroki.append(f"  и ещё {len(subiekty) - 5} субъектов")

    return "\n".join(stroki)


async def pokazateli_rosstata(ctx: Context) -> str:
    """Получить список основных показателей Росстата.

    Возвращает:
        Список доступных показателей.
    """
    await ctx.info("Запрос списка показателей Росстата...")

    stroki_tablitsy = [(p["kod"], p["nazvanie"]) for p in KLYUCHEVYE_INDIKATORY]
    header = "**Основные показатели Росстата**\n\n"
    return header + tablitsa_v_markdown(["Код", "Показатель"], stroki_tablitsy)


async def inflyaciya(god: str = "", ctx: Context | None = None) -> str:
    """Получить данные об инфляции (ИПЦ) в России.

    Аргументы:
        god: Год для запроса (например, '2025'). По умолчанию — текущий.

    Возвращает:
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
            f"используйте показатель 'ipcz' через API ЕМИСС."
        )
    stroki_tablitsy = []
    for d in data:
        ipcz_m = f"{d.get('ipcz_mesyac', '')}%" if d.get("ipcz_mesyac") else "—"
        ipcz_n = f"{d.get('ipcz_nakoplenny', '')}%" if d.get("ipcz_nakoplenny") else "—"
        ipcz_g = f"{d.get('ipcz_god', '')}%" if d.get("ipcz_god") else "—"
        stroki_tablitsy.append((d.get("period", ""), ipcz_m, ipcz_n, ipcz_g))
    header = "**Инфляция в России (ИПЦ)**\n\n"
    header += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return header + tablitsa_v_markdown(
        ["Период", "К мес.", "Накопл.", "К г/г"],
        stroki_tablitsy,
    )


async def demografiya(subiekt: str = "", ctx: Context | None = None) -> str:
    """Получить демографические данные по России или региону.

    Аргументы:
        subiekt: Код региона (необязательно).

    Возвращает:
        Демографические данные.
    """
    if ctx:
        await ctx.info("Запрос демографических данных...")
    data = await client.poluchit_demografiyu(subiekt=subiekt)
    filter_text = f" по региону {subiekt}" if subiekt else " по России"
    if not data:
        return (
            f"**Демографические данные{filter_text}**\n\n"
            f"Демографическая статистика (рождаемость, смертность, "
            f"численность населения) доступна через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/24133\n"
            f"- Росстат: https://rosstat.gov.ru/statistics/population\n\n"
            f"Для получения конкретных данных используйте API ЕМИСС."
        )
    stroki_tablitsy = []
    for d in data:
        nas = formatirovat_chislo_ru(d["naselenie"], 0) if d.get("naselenie") else "—"
        rozh = f"{d.get('rozhdaemost', '')}‰" if d.get("rozhdaemost") else "—"
        sm = f"{d.get('smertnost', '')}‰" if d.get("smertnost") else "—"
        stroki_tablitsy.append((d.get("period", ""), nas, rozh, sm))
    header = f"**Демографические данные{filter_text}**\n\n"
    header += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return header + tablitsa_v_markdown(
        ["Период", "Население", "Рожд.", "Смерт."],
        stroki_tablitsy,
    )


async def vrp_dannye(subiekt: str = "", god: str = "", ctx: Context | None = None) -> str:
    """Получить данные о валовом региональном продукте (ВРП).

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по всем регионам.
        god: Год для запроса (например, '2023').

    Возвращает:
        Данные о ВРП по России или региону.
    """
    if ctx:
        await ctx.info("Запрос данных о ВРП...")
    data = await client.poluchit_vrp(subiekt=subiekt, god=god)
    filter_text = f" по региону {subiekt}" if subiekt else ""
    if not data:
        return (
            f"**Валовой региональный продукт{filter_text}**\n\n"
            f"Данные о ВРП доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/26975\n"
            f"- Росстат: https://rosstat.gov.ru/vrp\n\n"
            f"Для получения конкретных данных используйте инструмент "
            f"с указанием кода региона и/или года."
        )
    stroki_tablitsy = []
    for d in data:
        vrp_val = formatirovat_chislo_ru(d.vrp, 2) if d.vrp else "—"
        vrp_pc = formatirovat_chislo_ru(d.vrp_na_dushu, 2) if d.vrp_na_dushu else "—"
        stroki_tablitsy.append((d.period, d.subiekt or "—", vrp_val, vrp_pc))
    header = f"**Валовой региональный продукт{filter_text}**\n\n"
    header += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return header + tablitsa_v_markdown(
        ["Период", "Регион", "ВРП (млрд ₽)", "ВРП на душу (тыс. ₽)"],
        stroki_tablitsy,
    )


async def zarplata_dannye(subiekt: str = "", god: str = "", ctx: Context | None = None) -> str:
    """Получить данные о средней заработной плате.

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по России.
        god: Год для запроса (например, '2024').

    Возвращает:
        Данные о заработной плате.
    """
    if ctx:
        await ctx.info("Запрос данных о заработной плате...")
    data = await client.poluchit_zarplatu(subiekt=subiekt, god=god)
    filter_text = f" по региону {subiekt}" if subiekt else " по России"
    if not data:
        return (
            f"**Средняя заработная плата{filter_text}**\n\n"
            f"Данные о заработной плате доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/24140\n"
            f"- Росстат: https://rosstat.gov.ru/labor\n\n"
            f"Для получения конкретных данных используйте инструмент "
            f"с указанием кода региона и/или года."
        )
    stroki_tablitsy = []
    for d in data:
        zp = formatirovat_chislo_ru(d.nominalnaya_zp, 2) if d.nominalnaya_zp else "—"
        real = f"{d.realnaya_zp_izmenenie}%" if d.realnaya_zp_izmenenie else "—"
        stroki_tablitsy.append((d.period, d.subiekt or "—", zp, real))
    header = f"**Средняя заработная плата{filter_text}**\n\n"
    header += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return header + tablitsa_v_markdown(
        ["Период", "Регион", "Номин. (₽)", "Реальн. изм."],
        stroki_tablitsy,
    )


async def sravnenie_regionov(pokazatel: str, ctx: Context) -> str:
    """Сравнить регионы по выбранному показателю.

    Аргументы:
        pokazatel: Код показателя (например, 'vrp', 'zarplata', 'dokhody_na_dushu').

    Возвращает:
        Рейтинг регионов по показателю.
    """
    await ctx.info(f"Запрос сравнения регионов по показателю '{pokazatel}'...")
    if pokazatel not in REGIONALNYE_POKAZATELI:
        available = ", ".join(sorted(REGIONALNYE_POKAZATELI.keys()))
        return (
            f"Показатель '{pokazatel}' не поддерживается для регионального сравнения.\n\n"
            f"Доступные показатели: {available}"
        )
    data = await client.poluchit_sravnenie_regionov(pokazatel)
    if not data:
        emiss_code = REGIONALNYE_POKAZATELI[pokazatel]
        return (
            f"**Сравнение регионов по показателю '{pokazatel}'**\n\n"
            f"Данные временно недоступны.\n"
            f"ЕМИСС: https://fedstat.ru/indicator/{emiss_code}"
        )
    sorted_data = sorted(data, key=lambda x: x.get("znachenie") or 0, reverse=True)
    stroki_tablitsy = []
    for i, d in enumerate(sorted_data, 1):
        val = formatirovat_chislo_ru(d["znachenie"], 2) if d.get("znachenie") else "—"
        stroki_tablitsy.append(
            (i, d.get("subiekt", "—"), d.get("kod", "—"), val, d.get("period", "—"))
        )
    imya_indikatora = next(
        (p["nazvanie"] for p in KLYUCHEVYE_INDIKATORY if p["kod"] == pokazatel),
        pokazatel,
    )
    header = f"**Рейтинг регионов по показателю «{imya_indikatora}»**\n\n"
    header += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return header + tablitsa_v_markdown(
        ["№", "Регион", "Код", "Значение", "Период"],
        stroki_tablitsy,
    )


async def indikator_dannye(
    kod: str,
    subiekt: str = "",
    god: str = "",
    ctx: Context | None = None,
) -> str:
    """Получить данные произвольного показателя Росстата по коду ЕМИСС.

    Универсальный инструмент для запроса данных по любому известному коду ЕМИСС
    или мнемоническому коду показателя.

    Аргументы:
        kod: Код ЕМИСС (например, '31088') или мнемонический код (например, 'ipcz', 'vrp').
        subiekt: Код региона (необязательно).
        god: Год для запроса (например, '2024').

    Возвращает:
        Данные показателя.
    """
    if ctx:
        await ctx.info(f"Запрос данных показателя '{kod}'...")
    emiss_code = EMISS_KODY_POKAZATELEY.get(kod, kod)
    imya_indikatora = next(
        (p["nazvanie"] for p in KLYUCHEVYE_INDIKATORY if p["kod"] == kod),
        "",
    )
    if not imya_indikatora and kod in EMISS_KODY_POKAZATELEY:
        imya_indikatora = next(
            (p["nazvanie"] for p in KLYUCHEVYE_INDIKATORY if p["kod"] == kod),
            f"Показатель ЕМИСС {emiss_code}",
        )
    data = await client.poluchit_indikator_dannye(kod=kod, subiekt=subiekt, god=god)
    filter_parts = []
    if subiekt:
        filter_parts.append(f"регион {subiekt}")
    if god:
        filter_parts.append(f"год {god}")
    filter_text = f" ({', '.join(filter_parts)})" if filter_parts else ""
    if not data:
        return (
            f"**{imya_indikatora or kod}**{filter_text}\n\n"
            f"Данные временно недоступны.\n"
            f"ЕМИСС: https://fedstat.ru/indicator/{emiss_code}\n\n"
            f"Мнемонические коды: {', '.join(sorted(EMISS_KODY_POKAZATELEY.keys()))}"
        )
    stroki_tablitsy = []
    for d in data:
        val = formatirovat_chislo_ru(d.znachenie, 2) if d.znachenie is not None else "—"
        stroki_tablitsy.append((d.period, d.subiekt or "—", val, d.edinitsa or "—"))
    title = imya_indikatora or f"Показатель ЕМИСС {emiss_code}"
    header = f"**{title}**{filter_text}\n\n"
    header += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return header + tablitsa_v_markdown(
        ["Период", "Регион", "Значение", "Ед. изм."],
        stroki_tablitsy,
    )


async def otraslevaya_struktura_vrp(
    subiekt: str = "",
    god: str = "",
    ctx: Context | None = None,
) -> str:
    """Получить отраслевую структуру ВРП по видам экономической деятельности (ОКВЭД).

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по России.
        god: Год для запроса (например, '2023').

    Возвращает:
        Отраслевая структура ВРП.
    """
    if ctx:
        await ctx.info("Запрос отраслевой структуры ВРП...")
    data = await client.poluchit_otraslevuyu_strukturu_vrp(subiekt=subiekt, god=god)
    filter_text = f" по региону {subiekt}" if subiekt else " по России"
    if not data:
        return (
            f"**Отраслевая структура ВРП{filter_text}**\n\n"
            f"Данные доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/27103\n"
            f"- Росстат: https://rosstat.gov.ru/vrp\n\n"
            f"Разделы ОКВЭД: "
            + ", ".join(f"{o['kod']} — {o['nazvanie']}" for o in OTRASLEVAYA_STRUKTURA_VRP)
        )
    stroki_tablitsy = []
    for d in data:
        dolya = f"{d.dolya_vvp:.1f}%" if d.dolya_vvp is not None else "—"
        vrp_val = formatirovat_chislo_ru(d.vrp, 2) if d.vrp is not None else "—"
        stroki_tablitsy.append((d.kod_okved, d.otrasl, vrp_val, dolya))
    header = f"**Отраслевая структура ВРП{filter_text}**\n\n"
    header += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return header + tablitsa_v_markdown(
        ["ОКВЭД", "Отрасль", "ВРП (млрд ₽)", "Доля (%)"],
        stroki_tablitsy,
    )


async def investitsii_po_vidam(
    subiekt: str = "",
    god: str = "",
    ctx: Context | None = None,
) -> str:
    """Получить инвестиции в основной капитал по видам экономической деятельности.

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по России.
        god: Год для запроса (например, '2023').

    Возвращает:
        Инвестиции по видам деятельности.
    """
    if ctx:
        await ctx.info("Запрос инвестиций по видам деятельности...")
    data = await client.poluchit_investitsii_po_vidam(subiekt=subiekt, god=god)
    filter_text = f" по региону {subiekt}" if subiekt else " по России"
    if not data:
        return (
            f"**Инвестиции по видам деятельности{filter_text}**\n\n"
            f"Данные доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/24145\n"
            f"- Росстат: https://rosstat.gov.ru/investment\n\n"
            f"Виды деятельности: "
            + ", ".join(f"{v['kod']} — {v['nazvanie']}" for v in VIDY_DEYATELNOSTI_INVESTITSII)
        )
    stroki_tablitsy = []
    for d in data:
        inv_val = formatirovat_chislo_ru(d.investitsii, 2) if d.investitsii is not None else "—"
        dolya = f"{d.dolya:.1f}%" if d.dolya is not None else "—"
        stroki_tablitsy.append((d.kod_okved, d.vid_deyatelnosti, inv_val, dolya))
    header = f"**Инвестиции по видам деятельности{filter_text}**\n\n"
    header += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return header + tablitsa_v_markdown(
        ["ОКВЭД", "Вид деятельности", "Инвестиции (млрд ₽)", "Доля (%)"],
        stroki_tablitsy,
    )
