"""Инструменты модуля ГИБДД/МВД."""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

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

    Возвращает:
        Список типов ТС (легковой, грузовой, автобус, мотоцикл и т.д.).
    """
    stroki_tablitsy = [(t["kod"], t["nazvanie"]) for t in TipyTransportnykhSredstv]
    return tablitsa_v_markdown(["Код", "Тип ТС"], stroki_tablitsy)


async def spisok_kategoriyy_vu(ctx: Context) -> str:
    """Список категорий водительских удостоверений.

    Возвращает:
        Список категорий ВУ (A, B, C, D, M и т.д.).
    """
    stroki_tablitsy = [(k["kod"], k["nazvanie"]) for k in KategoriiVoditelskihUdostovereniy]
    return tablitsa_v_markdown(["Категория", "Описание"], stroki_tablitsy)


async def spisok_vidov_narusheniy(ctx: Context) -> str:
    """Список видов нарушений ПДД.

    Возвращает:
        Список нарушений (скорость, красный свет, пешеходы и т.д.).
    """
    stroki_tablitsy = [(n["kod"], n["nazvanie"]) for n in VidyNarusheniy]
    return tablitsa_v_markdown(["Код", "Вид нарушения"], stroki_tablitsy)


async def spisok_statusov_shtrafov(ctx: Context) -> str:
    """Список статусов штрафов ГИБДД.

    Возвращает:
        Список статусов (не оплачен, оплачен, передан приставам и т.д.).
    """
    stroki_tablitsy = [(s["kod"], s["nazvanie"]) for s in StatusyShtrafov]
    return tablitsa_v_markdown(["Код", "Статус штрафа"], stroki_tablitsy)


async def spisok_tipov_dtp(ctx: Context) -> str:
    """Список типов ДТП.

    Возвращает:
        Список типов ДТП (столкновение, налёт на пешехода и т.д.).
    """
    stroki_tablitsy = [(t["kod"], t["nazvanie"]) for t in TipyDTP]
    return tablitsa_v_markdown(["Код", "Тип ДТП"], stroki_tablitsy)


async def spisok_regionov_registratsii(ctx: Context) -> str:
    """Список основных регионов регистрации ТС.

    Возвращает:
        Список регионов с кодами.
    """
    stroki_tablitsy = [(r["kod"], r["nazvanie"]) for r in RegionyRegistratsii]
    return tablitsa_v_markdown(["Код региона", "Регион"], stroki_tablitsy)


async def info_ts(ctx: Context, vin: str) -> str:
    """Проверка транспортного средства по VIN.

    Аргументы:
        vin: VIN-номер транспортного средства (17 символов).

    Возвращает:
        Сведения о ТС: история регистраций, розыск, ограничения, ДТП.
    """
    history, dtp, razyskivaemye, restrict = await _polnaya_proverka_ts(vin)

    stroki = [f"**Транспортное средство** (VIN: {vin})"]

    if history:
        stroki.append(f"\n**История регистраций** ({len(history)} записей)")
        stroki_tablitsy = [
            (r.data_deystviya, r.tip_deystviya, r.gos_nomer, r.subiekt) for r in history
        ]
        stroki.append(
            tablitsa_v_markdown(["Дата", "Действие", "Госномер", "Регион"], stroki_tablitsy)
        )
    else:
        stroki.append("\nИстория регистраций: данные не найдены.")

    if dtp:
        stroki.append(f"\n**ДТП** ({len(dtp)} записей)")
        stroki_tablitsy = [
            (d["data_dtp"], d["tip_dtp"], d["region_dtp"], d["model_ts"]) for d in dtp
        ]
        stroki.append(
            tablitsa_v_markdown(["Дата ДТП", "Тип", "Регион", "Модель ТС"], stroki_tablitsy)
        )
    else:
        stroki.append("\nДТП: данные не найдены.")

    if razyskivaemye:
        stroki.append(f"\n**⚠ Розыск** ({len(razyskivaemye)} записей)")
        stroki_tablitsy = [
            (w["data_rozyska"], w["subiekt"], w["initsiator"], w["model_ts"])
            for w in razyskivaemye
        ]
        stroki.append(
            tablitsa_v_markdown(["Дата", "Регион", "Инициатор", "Модель ТС"], stroki_tablitsy)
        )
    else:
        stroki.append("\nРозыск: не числится.")

    if restrict:
        stroki.append(f"\n**⚠ Ограничения** ({len(restrict)} записей)")
        stroki_tablitsy = [
            (r["data_ogranicheniya"], r["tip_ogranicheniya"], r["subiekt"], r["initsiator"])
            for r in restrict
        ]
        stroki.append(
            tablitsa_v_markdown(
                ["Дата", "Тип ограничения", "Регион", "Инициатор"], stroki_tablitsy
            )
        )
    else:
        stroki.append("\nОграничения: не найдены.")

    return "\n".join(stroki) + _ATTRIBUTION


async def _polnaya_proverka_ts(vin: str) -> tuple:
    """Выполнение всех проверок транспортного средства параллельно."""
    import asyncio

    rezultaty = await asyncio.gather(
        client.proverka_istorii_ts(vin),
        client.proverka_dtp_ts(vin),
        client.proverka_rozysk_ts(vin),
        client.proverka_ogranicheniy_ts(vin),
    )
    return rezultaty


async def info_vu(ctx: Context, nomer_vu: str) -> str:
    """Проверка водительского удостоверения.

    Аргументы:
        nomer_vu: Серия и номер ВУ (10 цифр, без пробелов).

    Возвращает:
        Сведения о ВУ (категория, срок, статус, ограничения).
    """
    vu = await client.proverka_vu(nomer_vu)
    if not vu:
        return f"Информация по ВУ {nomer_vu} не найдена." + _ATTRIBUTION

    stroki = [
        f"**Водительское удостоверение** (№ {nomer_vu})",
        f"- ФИО: {vu.fio}",
        f"- Категория: {vu.kategoriya}",
        f"- Дата выдачи: {vu.data_vydachi}",
        f"- Срок действия: {vu.srok_deystviya}",
        f"- Статус: {vu.sostoyanie or 'действительно'}",
        f"- Место рождения: {vu.mesto_rozhdeniya}",
        f"- Ограничения: {vu.ograniceniya or 'нет'}",
        f"- Особые отметки: {vu.osoboie_otmetki or 'нет'}",
    ]
    return "\n".join(stroki) + _ATTRIBUTION


async def shtrafy_po_ts(ctx: Context, gos_nomer: str) -> str:
    """Штрафы ГИБДД по госномеру транспортного средства.

    Проверка штрафов требует авторизованный доступ через Госуслуги.

    Аргументы:
        gos_nomer: Государственный регистрационный номер ТС (напр. «А123АА77»).

    Возвращает:
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

    Аргументы:
        nomer_vu: Серия и номер ВУ (10 цифр).

    Возвращает:
        Информация о штрафах или указание использовать Госуслуги.
    """
    return (
        f"Проверка штрафов по ВУ {nomer_vu} требует авторизацию "
        f"через Госуслуги: https://www.gosuslugi.ru/10001/1\n\n"
        f"Публичный API ГИБДД не предоставляет данные о штрафах без "
        f"авторизации. Используйте сайт Госуслуг или портал ГИБДД."
    ) + _ATTRIBUTION


async def statistika_dtp(ctx: Context, subiekt: str, god: int = 2024) -> str:
    """Статистика ДТП по региону.

    Аргументы:
        subiekt: Название субъекта РФ.
        god: Год статистики.

    Возвращает:
        Статистика ДТП: количество, погибшие, раненые, пешеходы, дети.
    """
    dannye = await client.statistika_dtp_region(subiekt, god)
    if not dannye:
        return f"Статистика ДТП по региону «{subiekt}» за {god} год не найдена." + _ATTRIBUTION

    stroki = [
        f"**Статистика ДТП** — {dannye.subiekt}, {dannye.god} г.",
        f"- Всего ДТП: {formatirovat_chislo_ru(dannye.kolichestvo_dtp, 0)}",
        f"- Погибшие: {formatirovat_chislo_ru(dannye.pogibshie, 0)}",
        f"- Раненые: {formatirovat_chislo_ru(dannye.ranennye, 0)}",
        f"- ДТП с пешеходами: {formatirovat_chislo_ru(dannye.dtp_s_peshchodami, 0)}",
        f"- ДТП с участием детей: {formatirovat_chislo_ru(dannye.dtp_s_detmi, 0)}",
        f"- ДТП по вине нетрезвых: {formatirovat_chislo_ru(dannye.alco_gibdd, 0)}",
    ]
    return "\n".join(stroki) + _ATTRIBUTION


async def istoriya_registraciy(ctx: Context, vin: str) -> str:
    """История регистрационных действий транспортного средства.

    Аргументы:
        vin: VIN-номер транспортного средства (17 символов).

    Возвращает:
        Список регистрационных действий (постановка/снятие с учёта, смена собственника).
    """
    zapisi = await client.proverka_istorii_ts(vin)
    if not zapisi:
        return f"История регистраций по VIN {vin} не найдена." + _ATTRIBUTION

    stroki_tablitsy = [(r.data_deystviya, r.tip_deystviya, r.gos_nomer, r.subiekt) for r in zapisi]
    return (
        tablitsa_v_markdown(["Дата", "Действие", "Госномер", "Регион"], stroki_tablitsy)
        + _ATTRIBUTION
    )
