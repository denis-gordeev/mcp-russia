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


async def spisok_regionov(kontekst: Context) -> str:
    """Получить список субъектов Российской Федерации.

    Возвращает:
        Список субъектов РФ с кодами.
    """
    await kontekst.info("Запрос списка субъектов РФ...")
    regiony = client.poluchit_spisok_subiektov()

    stroki_tablitsy = [
        (region["kod"], region["nazvanie"], region.get("okrug", "")) for region in regiony
    ]
    zagolovok = f"**Субъекты Российской Федерации** — {len(regiony)} субъектов\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Регион", "ФО"], stroki_tablitsy)


async def spisok_okrugov(kontekst: Context) -> str:
    """Получить список федеральных округов РФ.

    Возвращает:
        Список федеральных округов.
    """
    await kontekst.info("Запрос списка федеральных округов...")
    okruga = client.poluchit_spisok_federalnykh_okrugov()

    stroki_tablitsy = [(okrug["kod"], okrug["nazvanie"]) for okrug in okruga]
    zagolovok = "**Федеральные округа Российской Федерации**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Округ"], stroki_tablitsy)


async def informatsiya_o_regionye(kod: str, kontekst: Context) -> str:
    """Получить информацию о субъекте РФ по коду.

    Аргументы:
        kod: Код региона (OKATO).

    Возвращает:
        Информация о регионе.
    """
    await kontekst.info(f"Запрос информации о регионе {kod}...")
    dannye = await client.poluchit_dannye_regiona(kod)

    if not dannye:
        return (
            f"Регион с кодом '{kod}' не найден.\n\n"
            f"Используйте spisok_regionov() для списка субъектов."
        )

    stroki = [
        f"**{dannye.nazvanie}** (код {dannye.kod})",
    ]
    if dannye.federalny_okrug:
        stroki.append(f"- Федеральный округ: {dannye.federalny_okrug}")
    if dannye.naselenie:
        stroki.append(f"- Население: {formatirovat_chislo_ru(dannye.naselenie, 0)} чел.")
    if dannye.vrp:
        stroki.append(f"- ВРП: {formatirovat_chislo_ru(dannye.vrp, 2)} млрд ₽")
    if dannye.srednyaya_zp:
        stroki.append(f"- Средняя зарплата: {formatirovat_chislo_ru(dannye.srednyaya_zp, 2)} ₽")

    stroki.append("- Источник: Росстат / ЕМИСС (fedstat.ru)")
    return "\n".join(stroki)


async def informatsiya_ob_okruge(kod: str, kontekst: Context) -> str:
    """Получить информацию о федеральном округе.

    Аргументы:
        kod: Код федерального округа.

    Возвращает:
        Информация о федеральном округе.
    """
    await kontekst.info(f"Запрос информации о федеральном округе {kod}...")
    dannye = await client.poluchit_federalny_okrug(kod)

    if "oshibka" in dannye:
        return f"{dannye['oshibka']}\n\nИспользуйте spisok_okrugov() для списка округов."

    stroki = [
        f"**{dannye['nazvanie']}** (код {dannye['kod']})",
        f"- Субъектов в округе: {dannye.get('kolichestvo_subiektov', 0)}",
    ]
    subiekty = dannye.get("subiekty", [])
    if subiekty:
        stroki.append(f"- Субъекты: {', '.join(subiekty[:5])}")
        if len(subiekty) > 5:
            stroki.append(f"  и ещё {len(subiekty) - 5} субъектов")

    return "\n".join(stroki)


async def pokazateli_rosstata(kontekst: Context) -> str:
    """Получить список основных показателей Росстата.

    Возвращает:
        Список доступных показателей.
    """
    await kontekst.info("Запрос списка показателей Росстата...")

    stroki_tablitsy = [
        (pokazatel["kod"], pokazatel["nazvanie"]) for pokazatel in KLYUCHEVYE_INDIKATORY
    ]
    zagolovok = "**Основные показатели Росстата**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Показатель"], stroki_tablitsy)


async def inflyaciya(god: str = "", kontekst: Context | None = None) -> str:
    """Получить данные об инфляции (ИПЦ) в России.

    Аргументы:
        god: Год для запроса (например, '2025'). По умолчанию — текущий.

    Возвращает:
        Данные об инфляции.
    """
    if kontekst:
        await kontekst.info("Запрос данных об инфляции...")
    dannye = await client.poluchit_inflyaciyu(god)
    if not dannye:
        return (
            f"**Инфляция в России (ИПЦ)**\n\n"
            f"Данные об индексе потребительских цен доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/31088\n"
            f"- Росстат: https://rosstat.gov.ru/statistics/price\n\n"
            f"Для запроса данных за {god or 'текущий период'} "
            f"используйте показатель 'ipcz' через API ЕМИСС."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        ipcz_m = f"{zapis.get('ipcz_mesyac', '')}%" if zapis.get("ipcz_mesyac") else "—"
        ipcz_n = f"{zapis.get('ipcz_nakoplenny', '')}%" if zapis.get("ipcz_nakoplenny") else "—"
        ipcz_g = f"{zapis.get('ipcz_god', '')}%" if zapis.get("ipcz_god") else "—"
        stroki_tablitsy.append((zapis.get("period", ""), ipcz_m, ipcz_n, ipcz_g))
    zagolovok = "**Инфляция в России (ИПЦ)**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "К мес.", "Накопл.", "К г/г"],
        stroki_tablitsy,
    )


async def demografiya(subiekt: str = "", kontekst: Context | None = None) -> str:
    """Получить демографические данные по России или региону.

    Аргументы:
        subiekt: Код региона (необязательно).

    Возвращает:
        Демографические данные.
    """
    if kontekst:
        await kontekst.info("Запрос демографических данных...")
    dannye = await client.poluchit_demografiyu(subiekt=subiekt)
    tekst_filtra = f" по региону {subiekt}" if subiekt else " по России"
    if not dannye:
        return (
            f"**Демографические данные{tekst_filtra}**\n\n"
            f"Демографическая статистика (рождаемость, смертность, "
            f"численность населения) доступна через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/24133\n"
            f"- Росстат: https://rosstat.gov.ru/statistics/population\n\n"
            f"Для получения конкретных данных используйте API ЕМИСС."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        nas = formatirovat_chislo_ru(zapis["naselenie"], 0) if zapis.get("naselenie") else "—"
        rozh = f"{zapis.get('rozhdaemost', '')}‰" if zapis.get("rozhdaemost") else "—"
        sm = f"{zapis.get('smertnost', '')}‰" if zapis.get("smertnost") else "—"
        stroki_tablitsy.append((zapis.get("period", ""), nas, rozh, sm))
    zagolovok = f"**Демографические данные{tekst_filtra}**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Население", "Рожд.", "Смерт."],
        stroki_tablitsy,
    )


async def vrp_dannye(subiekt: str = "", god: str = "", kontekst: Context | None = None) -> str:
    """Получить данные о валовом региональном продукте (ВРП).

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по всем регионам.
        god: Год для запроса (например, '2023').

    Возвращает:
        Данные о ВРП по России или региону.
    """
    if kontekst:
        await kontekst.info("Запрос данных о ВРП...")
    dannye = await client.poluchit_vrp(subiekt=subiekt, god=god)
    tekst_filtra = f" по региону {subiekt}" if subiekt else ""
    if not dannye:
        return (
            f"**Валовой региональный продукт{tekst_filtra}**\n\n"
            f"Данные о ВРП доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/26975\n"
            f"- Росстат: https://rosstat.gov.ru/vrp\n\n"
            f"Для получения конкретных данных используйте инструмент "
            f"с указанием кода региона и/или года."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        vrp_val = formatirovat_chislo_ru(zapis.vrp, 2) if zapis.vrp else "—"
        vrp_pc = formatirovat_chislo_ru(zapis.vrp_na_dushu, 2) if zapis.vrp_na_dushu else "—"
        stroki_tablitsy.append((zapis.period, zapis.subiekt or "—", vrp_val, vrp_pc))
    zagolovok = f"**Валовой региональный продукт{tekst_filtra}**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Регион", "ВРП (млрд ₽)", "ВРП на душу (тыс. ₽)"],
        stroki_tablitsy,
    )


async def zarplata_dannye(
    subiekt: str = "", god: str = "", kontekst: Context | None = None
) -> str:
    """Получить данные о средней заработной плате.

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по России.
        god: Год для запроса (например, '2024').

    Возвращает:
        Данные о заработной плате.
    """
    if kontekst:
        await kontekst.info("Запрос данных о заработной плате...")
    dannye = await client.poluchit_zarplatu(subiekt=subiekt, god=god)
    tekst_filtra = f" по региону {subiekt}" if subiekt else " по России"
    if not dannye:
        return (
            f"**Средняя заработная плата{tekst_filtra}**\n\n"
            f"Данные о заработной плате доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/24140\n"
            f"- Росстат: https://rosstat.gov.ru/labor\n\n"
            f"Для получения конкретных данных используйте инструмент "
            f"с указанием кода региона и/или года."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        zp = formatirovat_chislo_ru(zapis.nominalnaya_zp, 2) if zapis.nominalnaya_zp else "—"
        real = f"{zapis.realnaya_zp_izmenenie}%" if zapis.realnaya_zp_izmenenie else "—"
        stroki_tablitsy.append((zapis.period, zapis.subiekt or "—", zp, real))
    zagolovok = f"**Средняя заработная плата{tekst_filtra}**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Регион", "Номин. (₽)", "Реальн. изм."],
        stroki_tablitsy,
    )


async def sravnenie_regionov(pokazatel: str, kontekst: Context) -> str:
    """Сравнить регионы по выбранному показателю.

    Аргументы:
        pokazatel: Код показателя (например, 'vrp', 'zarplata', 'dokhody_na_dushu').

    Возвращает:
        Рейтинг регионов по показателю.
    """
    await kontekst.info(f"Запрос сравнения регионов по показателю '{pokazatel}'...")
    if pokazatel not in REGIONALNYE_POKAZATELI:
        dostupnye = ", ".join(sorted(REGIONALNYE_POKAZATELI.keys()))
        return (
            f"Показатель '{pokazatel}' не поддерживается для регионального сравнения.\n\n"
            f"Доступные показатели: {dostupnye}"
        )
    dannye = await client.poluchit_sravnenie_regionov(pokazatel)
    if not dannye:
        kod_emiss = REGIONALNYE_POKAZATELI[pokazatel]
        return (
            f"**Сравнение регионов по показателю '{pokazatel}'**\n\n"
            f"Данные временно недоступны.\n"
            f"ЕМИСС: https://fedstat.ru/indicator/{kod_emiss}"
        )
    otsortirovannye_dannye = sorted(
        dannye, key=lambda zapis: zapis.get("znachenie") or 0, reverse=True
    )
    stroki_tablitsy = []
    for i, zapis in enumerate(otsortirovannye_dannye, 1):
        znachenie = (
            formatirovat_chislo_ru(zapis["znachenie"], 2) if zapis.get("znachenie") else "—"
        )
        stroki_tablitsy.append(
            (
                i,
                zapis.get("subiekt", "—"),
                zapis.get("kod", "—"),
                znachenie,
                zapis.get("period", "—"),
            )
        )
    imya_indikatora = next(
        (
            indikator["nazvanie"]
            for indikator in KLYUCHEVYE_INDIKATORY
            if indikator["kod"] == pokazatel
        ),
        pokazatel,
    )
    zagolovok = f"**Рейтинг регионов по показателю «{imya_indikatora}»**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Регион", "Код", "Значение", "Период"],
        stroki_tablitsy,
    )


async def indikator_dannye(
    kod: str,
    subiekt: str = "",
    god: str = "",
    kontekst: Context | None = None,
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
    if kontekst:
        await kontekst.info(f"Запрос данных показателя '{kod}'...")
    kod_emiss = EMISS_KODY_POKAZATELEY.get(kod, kod)
    imya_indikatora = next(
        (pokazatel["nazvanie"] for pokazatel in KLYUCHEVYE_INDIKATORY if pokazatel["kod"] == kod),
        "",
    )
    if not imya_indikatora and kod in EMISS_KODY_POKAZATELEY:
        imya_indikatora = next(
            (
                pokazatel["nazvanie"]
                for pokazatel in KLYUCHEVYE_INDIKATORY
                if pokazatel["kod"] == kod
            ),
            f"Показатель ЕМИСС {kod_emiss}",
        )
    dannye = await client.poluchit_indikator_dannye(kod=kod, subiekt=subiekt, god=god)
    chasti_filtra = []
    if subiekt:
        chasti_filtra.append(f"регион {subiekt}")
    if god:
        chasti_filtra.append(f"год {god}")
    tekst_filtra = f" ({', '.join(chasti_filtra)})" if chasti_filtra else ""
    if not dannye:
        return (
            f"**{imya_indikatora or kod}**{tekst_filtra}\n\n"
            f"Данные временно недоступны.\n"
            f"ЕМИСС: https://fedstat.ru/indicator/{kod_emiss}\n\n"
            f"Мнемонические коды: {', '.join(sorted(EMISS_KODY_POKAZATELEY.keys()))}"
        )
    stroki_tablitsy = []
    for zapis in dannye:
        znachenie = (
            formatirovat_chislo_ru(zapis.znachenie, 2) if zapis.znachenie is not None else "—"
        )
        stroki_tablitsy.append(
            (zapis.period, zapis.subiekt or "—", znachenie, zapis.edinitsa or "—")
        )
    zagolovok_tekst = imya_indikatora or f"Показатель ЕМИСС {kod_emiss}"
    zagolovok = f"**{zagolovok_tekst}**{tekst_filtra}\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Регион", "Значение", "Ед. изм."],
        stroki_tablitsy,
    )


async def otraslevaya_struktura_vrp(
    subiekt: str = "",
    god: str = "",
    kontekst: Context | None = None,
) -> str:
    """Получить отраслевую структуру ВРП по видам экономической деятельности (ОКВЭД).

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по России.
        god: Год для запроса (например, '2023').

    Возвращает:
        Отраслевая структура ВРП.
    """
    if kontekst:
        await kontekst.info("Запрос отраслевой структуры ВРП...")
    dannye = await client.poluchit_otraslevuyu_strukturu_vrp(subiekt=subiekt, god=god)
    tekst_filtra = f" по региону {subiekt}" if subiekt else " по России"
    if not dannye:
        return (
            f"**Отраслевая структура ВРП{tekst_filtra}**\n\n"
            f"Данные доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/27103\n"
            f"- Росстат: https://rosstat.gov.ru/vrp\n\n"
            f"Разделы ОКВЭД: "
            + ", ".join(
                f"{otrasl['kod']} — {otrasl['nazvanie']}" for otrasl in OTRASLEVAYA_STRUKTURA_VRP
            )
        )
    stroki_tablitsy = []
    for zapis in dannye:
        dolya = f"{zapis.dolya_vvp:.1f}%" if zapis.dolya_vvp is not None else "—"
        vrp_val = formatirovat_chislo_ru(zapis.vrp, 2) if zapis.vrp is not None else "—"
        stroki_tablitsy.append((zapis.kod_okved, zapis.otrasl, vrp_val, dolya))
    zagolovok = f"**Отраслевая структура ВРП{tekst_filtra}**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["ОКВЭД", "Отрасль", "ВРП (млрд ₽)", "Доля (%)"],
        stroki_tablitsy,
    )


async def investitsii_po_vidam(
    subiekt: str = "",
    god: str = "",
    kontekst: Context | None = None,
) -> str:
    """Получить инвестиции в основной капитал по видам экономической деятельности.

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по России.
        god: Год для запроса (например, '2023').

    Возвращает:
        Инвестиции по видам деятельности.
    """
    if kontekst:
        await kontekst.info("Запрос инвестиций по видам деятельности...")
    dannye = await client.poluchit_investitsii_po_vidam(subiekt=subiekt, god=god)
    tekst_filtra = f" по региону {subiekt}" if subiekt else " по России"
    if not dannye:
        return (
            f"**Инвестиции по видам деятельности{tekst_filtra}**\n\n"
            f"Данные доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/24145\n"
            f"- Росстат: https://rosstat.gov.ru/investment\n\n"
            f"Виды деятельности: "
            + ", ".join(
                f"{vid['kod']} — {vid['nazvanie']}" for vid in VIDY_DEYATELNOSTI_INVESTITSII
            )
        )
    stroki_tablitsy = []
    for zapis in dannye:
        inv_val = (
            formatirovat_chislo_ru(zapis.investitsii, 2) if zapis.investitsii is not None else "—"
        )
        dolya = f"{zapis.dolya:.1f}%" if zapis.dolya is not None else "—"
        stroki_tablitsy.append((zapis.kod_okved, zapis.vid_deyatelnosti, inv_val, dolya))
    zagolovok = f"**Инвестиции по видам деятельности{tekst_filtra}**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["ОКВЭД", "Вид деятельности", "Инвестиции (млрд ₽)", "Доля (%)"],
        stroki_tablitsy,
    )
