"""Инструменты модуля Росстата.

Инструменты для доступа к демографическим, экономическим и региональным данным Росстата.

Правила (CONTRIBUTING.md):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client
from .constants import (
    EMISS_KODY_POKAZATELEY,
    FEDERALNYE_OKRUGA,
    KLYUCHEVYE_INDIKATORY,
    NASELENIE_SUBIEKTOV,
    OTNOSITELNYE_POKAZATELI,
    OTRASLEVAYA_STRUKTURA_VRP,
    REGIONALNYE_POKAZATELI,
    SUBIEKTY_RF,
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
        (subiekt_rf["kod"], subiekt_rf["nazvanie"], subiekt_rf.get("okrug", ""))
        for subiekt_rf in regiony
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


async def poisk_regiona(podstroka: str, kontekst: Context) -> str:
    """Найти субъект РФ по подстроке названия.

    Аргументы:
        podstroka: Часть названия региона (без учёта регистра).

    Возвращает:
        Подходящие субъекты с кодами и федеральными округами.
    """
    await kontekst.info(f"Поиск региона по подстроке '{podstroka}'...")
    podstroka_nizh = podstroka.lower()
    naydennye = [
        subiekt_rf
        for subiekt_rf in SUBIEKTY_RF
        if podstroka_nizh in subiekt_rf["nazvanie"].lower()
    ]
    if not naydennye:
        return (
            f"По запросу '{podstroka}' субъекты не найдены.\n\n"
            f"Используйте spisok_regionov() для полного списка."
        )
    stroki_tablitsy = [
        (subiekt_rf["kod"], subiekt_rf["nazvanie"], subiekt_rf.get("okrug", ""))
        for subiekt_rf in naydennye
    ]
    zagolovok = f"**Найдено субъектов: {len(naydennye)}** по запросу «{podstroka}»\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Регион", "ФО"], stroki_tablitsy)


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
        (
            pokazatel["kod"],
            EMISS_KODY_POKAZATELEY.get(pokazatel["kod"], "—"),
            pokazatel["nazvanie"],
        )
        for pokazatel in KLYUCHEVYE_INDIKATORY
    ]
    zagolovok = "**Основные показатели Росстата**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "ЕМИСС", "Показатель"], stroki_tablitsy)


async def inflyatsiya(god: str = "", kontekst: Context | None = None) -> str:
    """Получить данные об инфляции (ИПЦ) в России.

    Аргументы:
        god: Год для запроса (например, '2025'). По умолчанию — текущий.

    Возвращает:
        Данные об инфляции.
    """
    if kontekst:
        await kontekst.info("Запрос данных об инфляции...")
    dannye = await client.poluchit_inflyatsiyu(god)
    if not dannye:
        return (
            f"**Инфляция в России (ИПЦ)**\n\n"
            f"Данные об индексе потребительских цен доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/31074\n"
            f"- Росстат: https://rosstat.gov.ru/statistics/price\n\n"
            f"Для запроса данных за {god or 'текущий период'} "
            f"используйте показатель 'ipcz' через API ЕМИСС."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        ipcz_m = f"{zapis.ipcz_mesyac}%" if zapis.ipcz_mesyac is not None else "—"
        ipcz_n = f"{zapis.ipcz_nakoplenny}%" if zapis.ipcz_nakoplenny is not None else "—"
        ipcz_g = f"{zapis.ipcz_god}%" if zapis.ipcz_god is not None else "—"
        stroki_tablitsy.append((zapis.period, ipcz_m, ipcz_n, ipcz_g))
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
            f"- ЕМИСС: https://fedstat.ru/indicator/31557\n"
            f"- Росстат: https://rosstat.gov.ru/statistics/population\n\n"
            f"Для получения конкретных данных используйте API ЕМИСС."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        nas = formatirovat_chislo_ru(zapis.naselenie, 0) if zapis.naselenie is not None else "—"
        rozh = f"{zapis.rozhdaemost}‰" if zapis.rozhdaemost is not None else "—"
        sm = f"{zapis.smertnost}‰" if zapis.smertnost is not None else "—"
        est = (
            f"{zapis.estestvenny_prirost:+.1f}‰" if zapis.estestvenny_prirost is not None else "—"
        )
        stroki_tablitsy.append((zapis.period, nas, rozh, sm, est))
    zagolovok = f"**Демографические данные{tekst_filtra}**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Население", "Рожд.", "Смерт.", "Ест. прирост"],
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
            f"- ЕМИСС: https://fedstat.ru/indicator/61497\n"
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
            f"- ЕМИСС: https://fedstat.ru/indicator/58701\n"
            f"- Росстат: https://rosstat.gov.ru/labor\n\n"
            f"Для получения конкретных данных используйте инструмент "
            f"с указанием кода региона и/или года."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        zp = formatirovat_chislo_ru(zapis.nominalnaya_zp, 2) if zapis.nominalnaya_zp else "—"
        realnoe_izmenenie = (
            f"{zapis.realnaya_zp_izmenenie}%" if zapis.realnaya_zp_izmenenie else "—"
        )
        stroki_tablitsy.append((zapis.period, zapis.subiekt or "—", zp, realnoe_izmenenie))
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
            (zapis.period, zapis.subiekt or "—", znachenie, zapis.edinitsa_izmereniya or "—")
        )
    zagolovok_tekst = imya_indikatora or f"Показатель ЕМИСС {kod_emiss}"
    zagolovok = f"**{zagolovok_tekst}**{tekst_filtra}\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Регион", "Значение", "Ед. изм."],
        stroki_tablitsy,
    )


async def dinamika_regiona(
    pokazatel: str,
    subiekt: str,
    god_nachalo: str = "",
    god_konets: str = "",
    kontekst: Context | None = None,
) -> str:
    """Получить динамику показателя Росстата для одного региона.

    Аргументы:
        pokazatel: Мнемонический код регионального показателя (например, 'vrp', 'zarplata').
        subiekt: Код региона из spisok_regionov().
        god_nachalo: Начальный год диапазона (необязательно).
        god_konets: Конечный год диапазона (необязательно).

    Возвращает:
        Хронологический ряд и изменение показателя между соседними периодами.
    """
    if kontekst:
        await kontekst.info(f"Запрос динамики показателя '{pokazatel}' для региона '{subiekt}'...")

    if pokazatel not in REGIONALNYE_POKAZATELI:
        dostupnye = ", ".join(sorted(REGIONALNYE_POKAZATELI))
        return (
            f"Показатель '{pokazatel}' не поддерживается для региональной динамики.\n\n"
            f"Доступные показатели: {dostupnye}"
        )

    info_subiekta = next(
        (region for region in SUBIEKTY_RF if region["kod"] == subiekt),
        None,
    )
    if info_subiekta is None:
        return (
            f"Регион с кодом '{subiekt}' не найден.\n\n"
            "Используйте spisok_regionov() для списка субъектов."
        )

    if god_nachalo and (len(god_nachalo) != 4 or not god_nachalo.isdigit()):
        return "Начальный год должен состоять из четырёх цифр, например '2020'."
    if god_konets and (len(god_konets) != 4 or not god_konets.isdigit()):
        return "Конечный год должен состоять из четырёх цифр, например '2024'."
    if god_nachalo and god_konets and god_nachalo > god_konets:
        return "Начальный год не может быть больше конечного."

    dannye = await client.poluchit_indikator_dannye(kod=pokazatel, subiekt=subiekt)
    dannye = [
        zapis
        for zapis in dannye
        if (not god_nachalo or zapis.period[:4] >= god_nachalo)
        and (not god_konets or zapis.period[:4] <= god_konets)
    ]
    dannye.sort(key=lambda zapis: zapis.period)

    kod_emiss = REGIONALNYE_POKAZATELI[pokazatel]
    nazvanie_pokazatelya = next(
        (
            indikator["nazvanie"]
            for indikator in KLYUCHEVYE_INDIKATORY
            if indikator["kod"] == pokazatel
        ),
        pokazatel,
    )
    if not dannye:
        return (
            f"**Динамика показателя «{nazvanie_pokazatelya}» — "
            f"{info_subiekta['nazvanie']}**\n\n"
            "Данные за выбранный период временно недоступны.\n"
            f"ЕМИСС: https://fedstat.ru/indicator/{kod_emiss}"
        )

    stroki_tablitsy = []
    predydushchee_znachenie: float | None = None
    for zapis in dannye:
        znachenie = (
            formatirovat_chislo_ru(zapis.znachenie, 2) if zapis.znachenie is not None else "—"
        )
        izmenenie = "—"
        if (
            zapis.znachenie is not None
            and predydushchee_znachenie is not None
            and predydushchee_znachenie != 0
        ):
            izmenenie = f"{(zapis.znachenie / predydushchee_znachenie - 1) * 100:+.2f}%"
        stroki_tablitsy.append(
            (zapis.period, znachenie, zapis.edinitsa_izmereniya or "—", izmenenie)
        )
        if zapis.znachenie is not None:
            predydushchee_znachenie = zapis.znachenie

    diapazon = ""
    if god_nachalo or god_konets:
        diapazon = f" ({god_nachalo or '…'}–{god_konets or '…'})"
    zagolovok = (
        f"**Динамика показателя «{nazvanie_pokazatelya}» — "
        f"{info_subiekta['nazvanie']}**{diapazon}\n\n"
        "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    )
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Значение", "Ед. изм.", "Изменение к пред. периоду"],
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
            f"- ЕМИСС: https://fedstat.ru/indicator/59450\n"
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
            f"- ЕМИСС: https://fedstat.ru/indicator/33644\n"
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


async def vvp_dannye(god: str = "", kontekst: Context | None = None) -> str:
    """Получить данные о валовом внутреннем продукте (ВВП) России.

    Аргументы:
        god: Год для запроса (например, '2024'). По умолчанию — последний доступный.

    Возвращает:
        Данные о ВВП России.
    """
    if kontekst:
        await kontekst.info("Запрос данных о ВВП...")
    dannye = await client.poluchit_indikator_dannye(kod="vvp", god=god)
    if not dannye:
        return (
            "**Валовой внутренний продукт (ВВП) России**\n\n"
            "Данные о ВВП доступны через:\n"
            "- ЕМИСС: https://fedstat.ru/indicator/60201\n"
            "- Росстат: https://rosstat.gov.ru/vvp\n\n"
            "Для запроса данных за конкретный год используйте параметр god."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        znachenie = (
            formatirovat_chislo_ru(zapis.znachenie, 2) if zapis.znachenie is not None else "—"
        )
        stroki_tablitsy.append((zapis.period, znachenie, zapis.edinitsa_izmereniya or "—"))
    zagolovok = "**Валовой внутренний продукт (ВВП) России**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "ВВП", "Ед. изм."],
        stroki_tablitsy,
    )


async def bezrabotitsa_dannye(
    subiekt: str = "", god: str = "", kontekst: Context | None = None
) -> str:
    """Получить данные об уровне безработицы.

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по России.
        god: Год для запроса (например, '2024').

    Возвращает:
        Данные об уровне безработицы.
    """
    if kontekst:
        await kontekst.info("Запрос данных о безработице...")
    dannye = await client.poluchit_indikator_dannye(kod="bezrabotitsa", subiekt=subiekt, god=god)
    tekst_filtra = f" по региону {subiekt}" if subiekt else " по России"
    if not dannye:
        return (
            f"**Уровень безработицы{tekst_filtra}**\n\n"
            f"Данные доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/43062\n"
            f"- Росстат: https://rosstat.gov.ru/labor\n\n"
            f"Для запроса данных за конкретный год используйте параметр god."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        znachenie = f"{zapis.znachenie:.1f}%" if zapis.znachenie is not None else "—"
        stroki_tablitsy.append((zapis.period, zapis.subiekt or "—", znachenie))
    zagolovok = f"**Уровень безработицы{tekst_filtra}**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Регион", "Уровень"],
        stroki_tablitsy,
    )


async def dokhody_na_dushu(
    subiekt: str = "", god: str = "", kontekst: Context | None = None
) -> str:
    """Получить данные о среднедушевых денежных доходах населения.

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по России.
        god: Год для запроса (например, '2024').

    Возвращает:
        Данные о среднедушевых доходах.
    """
    if kontekst:
        await kontekst.info("Запрос данных о доходах на душу населения...")
    dannye = await client.poluchit_indikator_dannye(
        kod="dokhody_na_dushu", subiekt=subiekt, god=god
    )
    tekst_filtra = f" по региону {subiekt}" if subiekt else " по России"
    if not dannye:
        return (
            f"**Среднедушевые денежные доходы{tekst_filtra}**\n\n"
            f"Данные доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/57039\n"
            f"- Росстат: https://rosstat.gov.ru/income\n\n"
            f"Для запроса данных за конкретный год используйте параметр god."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        znachenie = (
            formatirovat_chislo_ru(zapis.znachenie, 2) if zapis.znachenie is not None else "—"
        )
        stroki_tablitsy.append(
            (zapis.period, zapis.subiekt or "—", znachenie, zapis.edinitsa_izmereniya or "—")
        )
    zagolovok = f"**Среднедушевые денежные доходы{tekst_filtra}**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Регион", "Доходы", "Ед. изм."],
        stroki_tablitsy,
    )


async def promyshlennoe_proizvodstvo(god: str = "", kontekst: Context | None = None) -> str:
    """Получить данные об индексе промышленного производства.

    Аргументы:
        god: Год для запроса (например, '2024').

    Возвращает:
        Данные об индексе промышленного производства.
    """
    if kontekst:
        await kontekst.info("Запрос данных о промышленном производстве...")
    dannye = await client.poluchit_indikator_dannye(kod="promyshlennoe_proizvodstvo", god=god)
    if not dannye:
        return (
            "**Индекс промышленного производства**\n\n"
            "Данные доступны через:\n"
            "- ЕМИСС: https://fedstat.ru/indicator/43045\n"
            "- Росстат: https://rosstat.gov.ru/statistics/industry\n\n"
            "Для запроса данных за конкретный год используйте параметр god."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        znachenie = f"{zapis.znachenie:.1f}%" if zapis.znachenie is not None else "—"
        stroki_tablitsy.append((zapis.period, znachenie))
    zagolovok = "**Индекс промышленного производства**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Индекс (% к пред. году)"],
        stroki_tablitsy,
    )


async def uroven_bednosti(
    subiekt: str = "", god: str = "", kontekst: Context | None = None
) -> str:
    """Получить данные об уровне бедности (доля населения с доходами ниже прожиточного минимума).

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по России.
        god: Год для запроса (например, '2024').

    Возвращает:
        Данные об уровне бедности.
    """
    if kontekst:
        await kontekst.info("Запрос данных об уровне бедности...")
    dannye = await client.poluchit_indikator_dannye(
        kod="uroven_bednosti", subiekt=subiekt, god=god
    )
    tekst_filtra = f" по региону {subiekt}" if subiekt else " по России"
    if not dannye:
        return (
            f"**Уровень бедности{tekst_filtra}**\n\n"
            f"Данные доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/33460\n"
            f"- Росстат: https://rosstat.gov.ru/income\n\n"
            f"Для запроса данных за конкретный год используйте параметр god."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        znachenie = f"{zapis.znachenie:.1f}%" if zapis.znachenie is not None else "—"
        stroki_tablitsy.append((zapis.period, zapis.subiekt or "—", znachenie))
    zagolovok = f"**Уровень бедности{tekst_filtra}**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Регион", "Доля (%)"],
        stroki_tablitsy,
    )


async def srednyaya_pensiya(
    subiekt: str = "", god: str = "", kontekst: Context | None = None
) -> str:
    """Получить данные о среднем размере назначенных пенсий.

    Аргументы:
        subiekt: Код региона (необязательно). Без указания — данные по России.
        god: Год для запроса (например, '2024').

    Возвращает:
        Данные о среднем размере пенсий.
    """
    if kontekst:
        await kontekst.info("Запрос данных о средней пенсии...")
    dannye = await client.poluchit_indikator_dannye(
        kod="srednyaya_pensiya", subiekt=subiekt, god=god
    )
    tekst_filtra = f" по региону {subiekt}" if subiekt else " по России"
    if not dannye:
        return (
            f"**Средний размер назначенных пенсий{tekst_filtra}**\n\n"
            f"Данные доступны через:\n"
            f"- ЕМИСС: https://fedstat.ru/indicator/60440\n"
            f"- Росстат: https://rosstat.gov.ru/society\n\n"
            f"Для запроса данных за конкретный год используйте параметр god."
        )
    stroki_tablitsy = []
    for zapis in dannye:
        znachenie = (
            formatirovat_chislo_ru(zapis.znachenie, 2) if zapis.znachenie is not None else "—"
        )
        stroki_tablitsy.append(
            (zapis.period, zapis.subiekt or "—", znachenie, zapis.edinitsa_izmereniya or "—")
        )
    zagolovok = f"**Средний размер назначенных пенсий{tekst_filtra}**\n\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Период", "Регион", "Размер пенсии", "Ед. изм."],
        stroki_tablitsy,
    )


async def sravnenie_okrugov(pokazatel: str, kontekst: Context) -> str:
    """Сравнить федеральные округа по выбранному показателю.

    Аргументы:
        pokazatel: Код показателя (например, 'vrp', 'zarplata', 'dokhody_na_dushu').

    Возвращает:
        Рейтинг федеральных округов по показателю.
    """
    await kontekst.info(f"Запрос сравнения федеральных округов по показателю '{pokazatel}'...")
    if pokazatel not in REGIONALNYE_POKAZATELI:
        dostupnye = ", ".join(sorted(REGIONALNYE_POKAZATELI.keys()))
        return (
            f"Показатель '{pokazatel}' не поддерживается для сравнения округов.\n\n"
            f"Доступные показатели: {dostupnye}"
        )
    dannye_regiony = await client.poluchit_sravnenie_regionov(pokazatel)
    if not dannye_regiony:
        kod_emiss = REGIONALNYE_POKAZATELI[pokazatel]
        return (
            f"**Сравнение округов по показателю '{pokazatel}'**\n\n"
            f"Данные временно недоступны.\n"
            f"ЕМИСС: https://fedstat.ru/indicator/{kod_emiss}"
        )
    otnositelnyy = pokazatel in OTNOSITELNYE_POKAZATELI
    dannye_po_okrugam: dict[str, float] = {}
    vesa_po_okrugam: dict[str, float] = {}
    for zapis in dannye_regiony:
        kod_reg = zapis.get("kod", "")
        info_subiekta = next(
            (subiekt_rf for subiekt_rf in SUBIEKTY_RF if subiekt_rf["kod"] == str(kod_reg)),
            None,
        )
        if info_subiekta:
            kod_okruga = info_subiekta.get("okrug", "")
            znachenie = zapis.get("znachenie") or 0
            if kod_okruga not in dannye_po_okrugam:
                dannye_po_okrugam[kod_okruga] = 0.0
                vesa_po_okrugam[kod_okruga] = 0.0
            if otnositelnyy:
                ves = NASELENIE_SUBIEKTOV.get(str(kod_reg), 1.0)
                dannye_po_okrugam[kod_okruga] += znachenie * ves
                vesa_po_okrugam[kod_okruga] += ves
            else:
                dannye_po_okrugam[kod_okruga] += znachenie
    if otnositelnyy:
        for kod_okruga in dannye_po_okrugam:
            if vesa_po_okrugam.get(kod_okruga, 0) > 0:
                dannye_po_okrugam[kod_okruga] = (
                    dannye_po_okrugam[kod_okruga] / vesa_po_okrugam[kod_okruga]
                )
    if not dannye_po_okrugam:
        return (
            f"**Сравнение округов по показателю '{pokazatel}'**\n\n"
            f"Не удалось агрегировать данные по округам."
        )
    otsortirovannye = sorted(dannye_po_okrugam.items(), key=lambda x: x[1], reverse=True)
    imya_indikatora = next(
        (
            indikator["nazvanie"]
            for indikator in KLYUCHEVYE_INDIKATORY
            if indikator["kod"] == pokazatel
        ),
        pokazatel,
    )
    tip_agregatsii = "взвешенное среднее" if otnositelnyy else "сумма"
    nazvaniya_okrugov = {okrug["kod"]: okrug["nazvanie"] for okrug in FEDERALNYE_OKRUGA}
    stroki_tablitsy = []
    for i, (kod_okruga, znachenie) in enumerate(otsortirovannye, 1):
        nazvanie_okruga = nazvaniya_okrugov.get(kod_okruga, kod_okruga)
        znachenie_fmt = formatirovat_chislo_ru(znachenie, 2) if znachenie else "—"
        stroki_tablitsy.append((i, nazvanie_okruga, kod_okruga, znachenie_fmt))
    zagolovok = f"**Рейтинг федеральных округов по показателю «{imya_indikatora}»**\n\n"
    zagolovok += f"Агрегация: {tip_agregatsii}\n"
    zagolovok += "Источник: Росстат / ЕМИСС (fedstat.ru)\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["№", "Федеральный округ", "Код", "Значение"],
        stroki_tablitsy,
    )
