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
    data = await client.poluchit_organizaciyu(inn)

    if not data:
        return (
            f"Организация с ИНН '{inn}' не найдена.\n\n"
            f"Проверьте корректность ИНН на egrul.nalog.ru"
        )

    lines = [f"**{data.nazvanie}**\n"]
    lines.append(f"- ИНН: {data.inn}")
    if data.ogrn:
        lines.append(f"- ОГРН: {data.ogrn}")
    if data.polnoe_nazvanie and data.polnoe_nazvanie != data.nazvanie:
        lines.append(f"- Полное название: {data.polnoe_nazvanie}")
    if data.yuridicheskiy_adres:
        lines.append(f"- Юридический адрес: {data.yuridicheskiy_adres}")
    if data.data_registracii:
        lines.append(f"- Дата регистрации: {data.data_registracii}")
    if data.status:
        lines.append(f"- Статус: {data.status}")
    if data.vid_deyatelnosti:
        lines.append(f"- Основной вид деятельности: {data.vid_deyatelnosti}")
    if data.rukovoditel:
        lines.append(f"- Руководитель: {data.rukovoditel}")
    if data.ustroyennyy_kapital:
        lines.append(f"- Уставный капитал: {data.ustroyennyy_kapital}")
    lines.append("- Источник: ФНС / ЕГРЮЛ (egrul.nalog.ru)")
    return "\n".join(lines)


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
    data = await client.poluchit_ip(inn)

    if not data:
        return f"ИП с ИНН '{inn}' не найден.\n\nПроверьте корректность ИНН на egrul.nalog.ru"

    lines = [f"**{data.fio}** (ИП)\n"]
    lines.append(f"- ИНН: {data.inn}")
    if data.ogrnip:
        lines.append(f"- ОГРНИП: {data.ogrnip}")
    if data.data_registracii:
        lines.append(f"- Дата регистрации: {data.data_registracii}")
    if data.status:
        lines.append(f"- Статус: {data.status}")
    if data.vid_deyatelnosti:
        lines.append(f"- Основной вид деятельности: {data.vid_deyatelnosti}")
    lines.append("- Источник: ФНС / ЕГРИП (egrul.nalog.ru)")
    return "\n".join(lines)


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
    data = await client.poluchit_proverki(inn)

    if not data:
        return (
            f"Данные о налоговых проверках для ИНН '{inn}' недоступны.\n\n"
            f"Информация о проверках доступна через Личный кабинет налогоплательщика: lkfl2.nalog.ru\n\n"
            f"Планы проверок: pb.nalog.ru"
        )

    rows = [(p.tip_proverki, p.period_proverki, p.status) for p in data]
    header = f"**Налоговые проверки** — ИНН {inn}\n\n"
    return header + tablitsa_v_markdown(["Тип", "Период", "Статус"], rows)


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
    data = await client.poluchit_nachisleniya(inn, period)

    if not data:
        period_text = f" за период {period}" if period else ""
        return (
            f"Данные о налоговых начислениях для ИНН '{inn}'{period_text} недоступны.\n\n"
            f"Начисления доступны через Личный кабинет налогоплательщика: lkfl2.nalog.ru"
        )

    rows = [
        (n.vid_naloga, n.period, formatirovat_chislo_ru(n.summa, 2) if n.summa else "—")
        for n in data
    ]
    header = f"**Налоговые начисления** — ИНН {inn}\n\n"
    return header + tablitsa_v_markdown(["Вид налога", "Период", "Сумма"], rows)
