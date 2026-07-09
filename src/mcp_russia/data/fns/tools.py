"""Инструменты модуля ФНС.

Инструменты для доступа к налоговым данным, поиска организаций в ЕГРЮЛ/ЕГРИП
и справочной информации о налоговых режимах и типах инспекций.
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client
from .constants import (
    KategoriiNalogoplatelshchikov,
    NalogovyeRezhimy,
    StatusyOrganizacii,
    TipyProverok,
    VidyNalogov,
)


def spisok_nalogovyh_rezhimov() -> list[dict]:
    """Список режимов налогообложения в РФ.

    Возвращает:
        Список режимов (ОСНО, УСН, ЕНВД, ПСН, ЕСН, НПД).
    """
    return NalogovyeRezhimy


def spisok_vidov_nalogov() -> list[dict]:
    """Список основных видов налогов в РФ.

    Возвращает:
        Список видов налогов (НДС, НДФЛ, налог на прибыль и др.).
    """
    return VidyNalogov


def spisok_tipov_proverok() -> list[dict]:
    """Список типов налоговых проверок.

    Возвращает:
        Список типов проверок (выездная, камеральная, документарная).
    """
    return TipyProverok


def spisok_statusov_organizaciy() -> list[dict]:
    """Список статусов организаций в ЕГРЮЛ.

    Возвращает:
        Список статусов (действующая, ликвидирована и т.д.).
    """
    return StatusyOrganizacii


def spisok_kategoriy_nalogoplatelshchikov() -> list[dict]:
    """Список категорий налогоплательщиков.

    Возвращает:
        Список категорий (юрлицо, ИП, самозанятый, физлицо).
    """
    return KategoriiNalogoplatelshchikov


async def info_organizacii(inn: str, ctx: Context | None = None) -> str:
    """Подробная информация об организации из ЕГРЮЛ.

    Использует публичный API egrul.nalog.ru для получения данных.

    Аргументы:
        inn: ИНН организации (10 цифр).

    Возвращает:
        Сведения об организации (название, адрес, руководитель, статус).
    """
    if ctx:
        await ctx.info(f"Запрос данных ЕГРЮЛ по ИНН {inn}...")
    dannye = await client.poluchit_organizaciyu(inn)

    if not dannye:
        return (
            f"Организация с ИНН '{inn}' не найдена.\n\n"
            f"Проверьте корректность ИНН на egrul.nalog.ru"
        )

    stroki = [f"**{dannye.nazvanie}**\n"]
    stroki.append(f"- ИНН: {dannye.inn}")
    if dannye.ogrn:
        stroki.append(f"- ОГРН: {dannye.ogrn}")
    if dannye.polnoe_nazvanie and dannye.polnoe_nazvanie != dannye.nazvanie:
        stroki.append(f"- Полное название: {dannye.polnoe_nazvanie}")
    if dannye.yuridicheskiy_adres:
        stroki.append(f"- Юридический адрес: {dannye.yuridicheskiy_adres}")
    if dannye.data_registracii:
        stroki.append(f"- Дата регистрации: {dannye.data_registracii}")
    if dannye.sostoyanie:
        stroki.append(f"- Статус: {dannye.sostoyanie}")
    if dannye.vid_deyatelnosti:
        stroki.append(f"- Основной вид деятельности: {dannye.vid_deyatelnosti}")
    if dannye.rukovoditel:
        stroki.append(f"- Руководитель: {dannye.rukovoditel}")
    if dannye.ustroyennyy_kapital:
        stroki.append(f"- Уставный капитал: {dannye.ustroyennyy_kapital}")
    stroki.append("- Источник: ФНС / ЕГРЮЛ (egrul.nalog.ru)")
    return "\n".join(stroki)


async def info_ip(inn: str, ctx: Context | None = None) -> str:
    """Подробная информация об ИП из ЕГРИП.

    Использует публичный API egrul.nalog.ru для получения данных.

    Аргументы:
        inn: ИНН индивидуального предпринимателя (12 цифр).

    Возвращает:
        Сведения об ИП (ФИО, дата регистрации, статус, вид деятельности).
    """
    if ctx:
        await ctx.info(f"Запрос данных ЕГРИП по ИНН {inn}...")
    dannye = await client.poluchit_ip(inn)

    if not dannye:
        return f"ИП с ИНН '{inn}' не найден.\n\nПроверьте корректность ИНН на egrul.nalog.ru"

    stroki = [f"**{dannye.fio}** (ИП)\n"]
    stroki.append(f"- ИНН: {dannye.inn}")
    if dannye.ogrnip:
        stroki.append(f"- ОГРНИП: {dannye.ogrnip}")
    if dannye.data_registracii:
        stroki.append(f"- Дата регистрации: {dannye.data_registracii}")
    if dannye.sostoyanie:
        stroki.append(f"- Статус: {dannye.sostoyanie}")
    if dannye.vid_deyatelnosti:
        stroki.append(f"- Основной вид деятельности: {dannye.vid_deyatelnosti}")
    stroki.append("- Источник: ФНС / ЕГРИП (egrul.nalog.ru)")
    return "\n".join(stroki)


async def proverki_organizacii(inn: str, ctx: Context | None = None) -> str:
    """Список налоговых проверок организации.

    Данные о проверках требуют авторизованный доступ к API ФНС.
    Возвращается справочная информация.

    Аргументы:
        inn: ИНН организации.

    Возвращает:
        Информация о проверках или справка.
    """
    if ctx:
        await ctx.info(f"Запрос данных о проверках по ИНН {inn}...")
    dannye = await client.poluchit_proverki(inn)

    if not dannye:
        return (
            f"Данные о налоговых проверках для ИНН '{inn}' недоступны.\n\n"
            f"Информация о проверках доступна через Личный кабинет налогоплательщика: lkfl2.nalog.ru\n\n"
            f"Планы проверок: pb.nalog.ru"
        )

    stroki_tablitsy = [(p.tip_proverki, p.period_proverki, p.sostoyanie) for p in dannye]
    zagolovok = f"**Налоговые проверки** — ИНН {inn}\n\n"
    return zagolovok + tablitsa_v_markdown(["Тип", "Период", "Статус"], stroki_tablitsy)


async def nalogovye_nachisleniya(inn: str, period: str = "", ctx: Context | None = None) -> str:
    """Налоговые начисления организации или ИП.

    Данные о начислениях требуют авторизованный доступ к API ФНС.
    Возвращается справочная информация.

    Аргументы:
        inn: ИНН организации или ИП.
        period: Налоговый период (необязательно, напр. «2025»).

    Возвращает:
        Информация о начислениях или справка.
    """
    if ctx:
        await ctx.info(f"Запрос данных о начислениях по ИНН {inn}...")
    dannye = await client.poluchit_nachisleniya(inn, period)

    if not dannye:
        period_tekst = f" за период {period}" if period else ""
        return (
            f"Данные о налоговых начислениях для ИНН '{inn}'{period_tekst} недоступны.\n\n"
            f"Начисления доступны через Личный кабинет налогоплательщика: lkfl2.nalog.ru"
        )

    stroki_tablitsy = [
        (n.vid_naloga, n.period, formatirovat_chislo_ru(n.summa, 2) if n.summa else "—")
        for n in dannye
    ]
    zagolovok = f"**Налоговые начисления** — ИНН {inn}\n\n"
    return zagolovok + tablitsa_v_markdown(["Вид налога", "Период", "Сумма"], stroki_tablitsy)
