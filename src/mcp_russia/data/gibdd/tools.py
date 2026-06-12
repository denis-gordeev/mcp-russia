"""Инструменты модуля ГИБДД/МВД."""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import format_number_ru, markdown_table

from . import client
from .constants import (
    KategoriiVoditelskihUdostovereniy,
    RegionyRegistratsii,
    StatusyShtrafov,
    TipyDTP,
    TipyTransportnykhSredstv,
    VidyNarusheniy,
)

_ATTRIBUTION = "\n\n_Источник: ГИБДД / МВД (гибдд.рф)_"


async def spisok_tipov_ts(ctx: Context) -> str:
    """Список типов транспортных средств.

    Returns:
        Список типов ТС (легковой, грузовой, автобус, мотоцикл и т.д.).
    """
    rows = [(t["code"], t["name"]) for t in TipyTransportnykhSredstv]
    return markdown_table(["Код", "Тип ТС"], rows)


async def spisok_kategoriyy_vu(ctx: Context) -> str:
    """Список категорий водительских удостоверений.

    Returns:
        Список категорий ВУ (A, B, C, D, M и т.д.).
    """
    rows = [(k["code"], k["name"]) for k in KategoriiVoditelskihUdostovereniy]
    return markdown_table(["Категория", "Описание"], rows)


async def spisok_vidov_narusheniy(ctx: Context) -> str:
    """Список видов нарушений ПДД.

    Returns:
        Список нарушений (скорость, красный свет, пешеходы и т.д.).
    """
    rows = [(n["code"], n["name"]) for n in VidyNarusheniy]
    return markdown_table(["Код", "Вид нарушения"], rows)


async def spisok_statusov_shtrafov(ctx: Context) -> str:
    """Список статусов штрафов ГИБДД.

    Returns:
        Список статусов (не оплачен, оплачен, передан приставам и т.д.).
    """
    rows = [(s["code"], s["name"]) for s in StatusyShtrafov]
    return markdown_table(["Код", "Статус штрафа"], rows)


async def spisok_tipov_dtp(ctx: Context) -> str:
    """Список типов ДТП.

    Returns:
        Список типов ДТП (столкновение, налёт на пешехода и т.д.).
    """
    rows = [(t["code"], t["name"]) for t in TipyDTP]
    return markdown_table(["Код", "Тип ДТП"], rows)


async def spisok_regionov_registratsii(ctx: Context) -> str:
    """Список основных регионов регистрации ТС.

    Returns:
        Список регионов с кодами.
    """
    rows = [(r["code"], r["name"]) for r in RegionyRegistratsii]
    return markdown_table(["Код региона", "Регион"], rows)


async def info_ts(ctx: Context, vin: str) -> str:
    """Проверка транспортного средства по VIN.

    Args:
        vin: VIN-номер транспортного средства (17 символов).

    Returns:
        Сведения о ТС: история регистраций, розыск, ограничения, ДТП.
    """
    history, dtp, wanted, restrict = await _proverka_ts_full(vin)

    lines = [f"**Транспортное средство** (VIN: {vin})"]

    if history:
        lines.append(f"\n**История регистраций** ({len(history)} записей)")
        rows = [(r.data_deystviya, r.tip_deystviya, r.gos_nomer, r.region) for r in history]
        lines.append(markdown_table(["Дата", "Действие", "Госномер", "Регион"], rows))
    else:
        lines.append("\nИстория регистраций: данные не найдены.")

    if dtp:
        lines.append(f"\n**ДТП** ({len(dtp)} записей)")
        rows = [(d["data_dtp"], d["tip_dtp"], d["region_dtp"], d["model_ts"]) for d in dtp]
        lines.append(markdown_table(["Дата ДТП", "Тип", "Регион", "Модель ТС"], rows))
    else:
        lines.append("\nДТП: данные не найдены.")

    if wanted:
        lines.append(f"\n**⚠ Розыск** ({len(wanted)} записей)")
        rows = [(w["data_rozyska"], w["region"], w["initiator"], w["model_ts"]) for w in wanted]
        lines.append(markdown_table(["Дата", "Регион", "Инициатор", "Модель ТС"], rows))
    else:
        lines.append("\nРозыск: не числится.")

    if restrict:
        lines.append(f"\n**⚠ Ограничения** ({len(restrict)} записей)")
        rows = [
            (r["data_ogranicheniya"], r["tip_ogranicheniya"], r["region"], r["initiator"])
            for r in restrict
        ]
        lines.append(markdown_table(["Дата", "Тип ограничения", "Регион", "Инициатор"], rows))
    else:
        lines.append("\nОграничения: не найдены.")

    return "\n".join(lines) + _ATTRIBUTION


async def _proverka_ts_full(vin: str) -> tuple:
    """Run all vehicle checks in parallel."""
    import asyncio

    results = await asyncio.gather(
        client.proverka_istorii_ts(vin),
        client.proverka_dtp_ts(vin),
        client.proverka_rozysk_ts(vin),
        client.proverka_ogranicheniy_ts(vin),
    )
    return results


async def info_vu(ctx: Context, nomer_vu: str) -> str:
    """Проверка водительского удостоверения.

    Args:
        nomer_vu: Серия и номер ВУ (10 цифр, без пробелов).

    Returns:
        Сведения о ВУ (категория, срок, статус, ограничения).
    """
    vu = await client.proverka_vu(nomer_vu)
    if not vu:
        return f"Информация по ВУ {nomer_vu} не найдена." + _ATTRIBUTION

    lines = [
        f"**Водительское удостоверение** (№ {nomer_vu})",
        f"- ФИО: {vu.fio}",
        f"- Категория: {vu.kategoriya}",
        f"- Дата выдачи: {vu.data_vydachi}",
        f"- Срок действия: {vu.srok_deystviya}",
        f"- Статус: {vu.status or 'действительно'}",
        f"- Место рождения: {vu.mesto_rozhdeniya}",
        f"- Ограничения: {vu.ograniceniya or 'нет'}",
        f"- Особые отметки: {vu.osoboie_otmetki or 'нет'}",
    ]
    return "\n".join(lines) + _ATTRIBUTION


async def shtrafy_po_ts(ctx: Context, gos_nomer: str) -> str:
    """Штрафы ГИБДД по госномеру транспортного средства.

    Проверка штрафов требует авторизованный доступ через Госуслуги.

    Args:
        gos_nomer: Государственный регистрационный номер ТС (напр. «А123АА77»).

    Returns:
        Информация о штрафах или указание использовать Госуслуги.
    """
    return (
        f"Проверка штрафов по госномеру {gos_nomer} требует авторизацию "
        f"через Госуслуги: https://www.gosuslugi.ru/10001/1\n\n"
        f"Публичный API ГИБДД не предоставляет данные о штрафах без "
        f"авторизации. Используйте сайт Госуслуг или портал ГИБДД."
    ) + _ATTRIBUTION


async def shtrafy_po_vu(ctx: Context, nomer_vu: str) -> str:
    """Штрафы ГИБДД по номеру водительского удостоверения.

    Проверка штрафов требует авторизованный доступ через Госуслуги.

    Args:
        nomer_vu: Серия и номер ВУ (10 цифр).

    Returns:
        Информация о штрафах или указание использовать Госуслуги.
    """
    return (
        f"Проверка штрафов по ВУ {nomer_vu} требует авторизацию "
        f"через Госуслуги: https://www.gosuslugi.ru/10001/1\n\n"
        f"Публичный API ГИБДД не предоставляет данные о штрафах без "
        f"авторизации. Используйте сайт Госуслуг или портал ГИБДД."
    ) + _ATTRIBUTION


async def statistika_dtp(ctx: Context, region: str, god: int = 2024) -> str:
    """Статистика ДТП по региону.

    Args:
        region: Название субъекта РФ.
        god: Год статистики.

    Returns:
        Статистика ДТП: количество, погибшие, раненые, пешеходы, дети.
    """
    data = await client.statistika_dtp_region(region, god)
    if not data:
        return f"Статистика ДТП по региону «{region}» за {god} год не найдена." + _ATTRIBUTION

    lines = [
        f"**Статистика ДТП** — {data.region}, {data.god} г.",
        f"- Всего ДТП: {format_number_ru(data.kolichestvo_dtp, 0)}",
        f"- Погибшие: {format_number_ru(data.pogibshie, 0)}",
        f"- Раненые: {format_number_ru(data.ranennye, 0)}",
        f"- ДТП с пешеходами: {format_number_ru(data.dtp_s_peshchodami, 0)}",
        f"- ДТП с участием детей: {format_number_ru(data.dtp_s_detmi, 0)}",
        f"- ДТП по вине нетрезвых: {format_number_ru(data.alco_gibdd, 0)}",
    ]
    return "\n".join(lines) + _ATTRIBUTION


async def istoriya_registraciy(ctx: Context, vin: str) -> str:
    """История регистрационных действий транспортного средства.

    Args:
        vin: VIN-номер транспортного средства (17 символов).

    Returns:
        Список регистрационных действий (постановка/снятие с учёта, смена собственника).
    """
    records = await client.proverka_istorii_ts(vin)
    if not records:
        return f"История регистраций по VIN {vin} не найдена." + _ATTRIBUTION

    rows = [(r.data_deystviya, r.tip_deystviya, r.gos_nomer, r.region) for r in records]
    return markdown_table(["Дата", "Действие", "Госномер", "Регион"], rows) + _ATTRIBUTION
