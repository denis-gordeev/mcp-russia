"""Инструменты модуля Росгидромета.

Инструменты для доступа к данным о погоде, климате, экологии и спутниковом мониторинге.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client


async def spisok_stanciy(kontekst: Context) -> str:
    """Получить список станций мониторинга Росгидромета.

    Возвращает:
        Список станций с кодами.
    """
    await kontekst.info("Запрос списка станций мониторинга...")
    stancii = client.poluchit_spisok_stantsiy()

    stroki_tablitsy = [
        (stantsiya["kod"], stantsiya["nazvanie"], stantsiya["subiekt"]) for stantsiya in stancii
    ]
    zagolovok = "**Станции мониторинга Росгидромета**\n\n"
    return zagolovok + tablitsa_v_markdown(["Код", "Город", "Округ"], stroki_tablitsy)


async def spisok_tipov_dannykh(kontekst: Context) -> str:
    """Получить список типов метеорологических и экологических данных.

    Возвращает:
        Список типов данных.
    """
    await kontekst.info("Запрос списка типов данных...")
    meteo = client.poluchit_spisok_tipov_meteo()
    eko = client.poluchit_spisok_tipov_eko()

    stroki = ["**Типы метеорологических данных**\n"]
    stroki_tablitsy = [(tip_meteo["kod"], tip_meteo["nazvanie"]) for tip_meteo in meteo]
    stroki.append(tablitsa_v_markdown(["Код", "Тип"], stroki_tablitsy))

    stroki.append("\n**Типы экологических данных**\n")
    stroki_tablitsy = [(tip_eko["kod"], tip_eko["nazvanie"]) for tip_eko in eko]
    stroki.append(tablitsa_v_markdown(["Код", "Тип"], stroki_tablitsy))

    return "\n".join(stroki)


async def pogoda_seychas(stanciya: str = "77", kontekst: Context | None = None) -> str:
    """Получить текущую погоду на станции.

    Аргументы:
        stanciya: Код станции (по умолчанию Москва — 77).

    Возвращает:
        Текущие погодные данные.
    """
    await kontekst.info(f"Запрос текущей погоды на станции {stanciya}...")
    dannye = await client.poluchit_pogodu(stanciya)

    if not dannye:
        return (
            f"Данные о погоде для станции '{stanciya}' недоступны.\n\n"
            f"Используйте spisok_stanciy() для списка станций."
        )

    stroki = [f"**Погода: {dannye.gorod}** ({dannye.subiekt})"]
    if dannye.temperatura:
        stroki.append(f"- Температура: {formatirovat_chislo_ru(dannye.temperatura, 1)}°C")
    if dannye.oshchushchaetsya_kak:
        stroki.append(
            f"- Ощущается как: {formatirovat_chislo_ru(dannye.oshchushchaetsya_kak, 1)}°C"
        )
    if dannye.vlazhnost:
        stroki.append(f"- Влажность: {formatirovat_chislo_ru(dannye.vlazhnost, 0)}%")
    if dannye.davlenie:
        stroki.append(f"- Давление: {formatirovat_chislo_ru(dannye.davlenie, 0)} мм рт.ст.")
    if dannye.veter_skorost:
        stroki.append(
            f"- Ветер: {formatirovat_chislo_ru(dannye.veter_skorost, 1)} м/с {dannye.veter_napravlenie}"
        )
    if dannye.osadki is not None:
        stroki.append(f"- Осадки: {formatirovat_chislo_ru(dannye.osadki, 1)} мм")
    if dannye.opisaniye:
        stroki.append(f"- Описание: {dannye.opisaniye}")
    if dannye.data_vremya:
        stroki.append(f"- Данные на: {dannye.data_vremya}")
    stroki.append("- Источник: Open-Meteo / Росгидромет")
    return "\n".join(stroki)


async def prognoz_pogody(
    stanciya: str = "77",
    dni: int = 3,
    kontekst: Context | None = None,
) -> str:
    """Получить прогноз погоды на несколько дней.

    Аргументы:
        stanciya: Код станции.
        dni: Количество дней прогноза (1-7).

    Возвращает:
        Прогноз погоды.
    """
    await kontekst.info(f"Запрос прогноза на {dni} дней для станции {stanciya}...")
    prognoz = await client.poluchit_prognoz(stanciya, dni)

    if not prognoz:
        return (
            f"Прогноз погоды для станции '{stanciya}' недоступен.\n\n"
            f"Используйте spisok_stanciy() для списка станций."
        )

    stroki = [f"**Прогноз погоды** — {len(prognoz)} дней\n"]
    for prognoz_item in prognoz:
        stroki.append(f"**{prognoz_item.data}**")
        if prognoz_item.temperatura_dnem is not None:
            stroki.append(f"- Днём: {formatirovat_chislo_ru(prognoz_item.temperatura_dnem, 1)}°C")
        if prognoz_item.temperatura_nochyu is not None:
            stroki.append(
                f"- Ночью: {formatirovat_chislo_ru(prognoz_item.temperatura_nochyu, 1)}°C"
            )
        if prognoz_item.osadki_veroyatnost is not None:
            stroki.append(
                f"- Осадки: {formatirovat_chislo_ru(prognoz_item.osadki_veroyatnost, 0)}%"
            )
        if prognoz_item.opisaniye:
            stroki.append(f"- {prognoz_item.opisaniye}")
        stroki.append("")

    stroki.append("- Источник: Open-Meteo / Росгидромет")
    return "\n".join(stroki)


async def ekologiya_regiona(
    gorod: str = "",
    tip: str = "",
    kontekst: Context | None = None,
) -> str:
    """Получить данные об экологической обстановке.

    Аргументы:
        gorod: Название города (необязательно).
        tip: Тип данных (vozdukh, voda, pochva, radiaciya, shum).

    Возвращает:
        Данные об экологической обстановке.
    """
    await kontekst.info(f"Запрос экологических данных: город={gorod}, тип={tip}")
    dannye = await client.poluchit_ekologiyu(gorod=gorod, tip=tip)

    if not dannye:
        filtry = []
        if gorod:
            filtry.append(f"город: {gorod}")
        if tip:
            filtry.append(f"тип: {tip}")
        tekst_filtra = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Экологические данные{tekst_filtra} недоступны.\n\n"
            f"Данные доступны на сайте Росприроднадзора: rpn.gov.ru"
        )

    stroki = [f"**Экологическая обстановка** — измерений: {len(dannye)}\n"]
    for zapis in dannye[:10]:
        stroka = f"- {zapis.gorod} ({zapis.tip}): {zapis.pokazatel}"
        if zapis.znachenie is not None:
            stroka += f" = {formatirovat_chislo_ru(zapis.znachenie, 2)}"
        if zapis.prevyshenie:
            stroka += " ⚠️ ПРЕВЫШЕНИЕ нормы"
        stroki.append(stroka)

    if len(dannye) > 10:
        stroki.append(f"\n... и ещё {len(dannye) - 10} измерений")

    stroki.append("- Источник: Open-Meteo Air Quality")
    return "\n".join(stroki)


async def preduprezhdeniya(subiekt: str = "", kontekst: Context | None = None) -> str:
    """Получить активные предупреждения об опасных явлении.

    Аргументы:
        subiekt: Регион (необязательно).

    Возвращает:
        Активные предупреждения.
    """
    await kontekst.info(f"Запрос предупреждений для региона {subiekt}...")
    dannye = await client.poluchit_preduprezhdeniya(subiekt)

    if not dannye:
        tekst_regiona = f" для региона '{subiekt}'" if subiekt else ""
        return (
            f"Активные предупреждения{tekst_regiona} отсутствуют.\n\n"
            f"Метеорологические данные: open-meteo.com / meteorf.ru"
        )

    stroki = [f"**Активные предупреждения** — {len(dannye)}\n"]
    for preduprezhdenie in dannye:
        stroki.append(
            f"⚠️ **{preduprezhdenie.tip}** — {preduprezhdenie.subiekt}, {preduprezhdenie.gorod}"
        )
        stroki.append(f"   {preduprezhdenie.opisanie}")
        if preduprezhdenie.data_nachala:
            stroki.append(f"   С: {preduprezhdenie.data_nachala}")
        if preduprezhdenie.data_okonchaniya:
            stroki.append(f"   По: {preduprezhdenie.data_okonchaniya}")
        stroki.append(f"   Уровень опасности: {preduprezhdenie.uroven_opasnosti}")
        stroki.append("")

    stroki.append("- Источник: Open-Meteo / Росгидромет")
    return "\n".join(stroki)


async def sputnik_monitoring(
    subiekt: str = "",
    tip: str = "",
    kontekst: Context | None = None,
) -> str:
    """Получить данные спутникового мониторинга.

    Аргументы:
        subiekt: Регион (необязательно).
        tip: Тип данных (lesa, voda, pozhary, snezhnyy_pokrov).

    Возвращает:
        Данные спутникового мониторинга.
    """
    await kontekst.info(f"Запрос спутниковых данных: регион={subiekt}, тип={tip}")
    dannye = await client.poluchit_sputnik_dannye(subiekt, tip)

    if not dannye:
        filtry = []
        if subiekt:
            filtry.append(f"регион: {subiekt}")
        if tip:
            filtry.append(f"тип: {tip}")
        tekst_filtra = f" ({', '.join(filtry)})" if filtry else ""
        return (
            f"Данные спутникового мониторинга{tekst_filtra} недоступны.\n\n"
            f"Спутниковые данные: niikp-atm.ru"
        )

    stroki = [f"**Спутниковый мониторинг** — снимков: {len(dannye)}\n"]
    for snimok in dannye[:5]:
        stroki.append(f"- {snimok.subiekt} ({snimok.data_syomki}): {snimok.tip_dannykh}")
        stroki.append(f"  Спутник: {snimok.sputnik}, Разрешение: {snimok.razreshenie}")
        if snimok.izobrazhenie_ssylka:
            stroki.append(f"  Изображение: {snimok.izobrazhenie_ssylka}")
        stroki.append("")

    if len(dannye) > 5:
        stroki.append(f"\n... и ещё {len(dannye) - 5} снимков")

    stroki.append("- Источник: Росгидромет / НИИ КП")
    return "\n".join(stroki)
