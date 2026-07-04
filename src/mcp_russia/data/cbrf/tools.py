"""Инструменты модуля ЦБ РФ.

Инструменты для доступа к курсам валют, ключевой ставке и экономическим индикаторам ЦБ.

Правила (ADR-001):
    - tools.py НЕ делает HTTP-запросы напрямую — делегирует client.py
    - Возвращает форматированные строки для LLM
"""

from __future__ import annotations

from fastmcp import Context

from mcp_russia._shared.formatting import formatirovat_chislo_ru, tablitsa_v_markdown

from . import client
from .constants import VALYUTY_PO_STRANAM


async def tekushchie_kursy(ctx: Context) -> str:
    """Получить официальные курсы основных валют ЦБ РФ на сегодня.

    Возвращает курсы: доллар США, евро, китайский юань,
    фунт стерлингов, японская иена, швейцарский франк.

    Возвращает:
        Таблица с курсами валют.
    """
    await ctx.info("Запрос курсов основных валют ЦБ РФ...")
    valyuty = await client.poluchit_osnovnye_valyuty()

    if not valyuty:
        return "Не удалось получить курсы валют ЦБ РФ."

    stroki_tablitsy = []
    for m in valyuty:
        izmenenie = ""
        if m.predydushchee_znachenie is not None and m.predydushchee_znachenie > 0:
            raznitsa = m.znachenie - m.predydushchee_znachenie
            znak = "+" if raznitsa >= 0 else ""
            protsent = (raznitsa / m.predydushchee_znachenie) * 100
            izmenenie = (
                f"{znak}{formatirovat_chislo_ru(raznitsa, 4)}"
                f" ({znak}{formatirovat_chislo_ru(protsent, 2)}%)"
            )
        else:
            izmenenie = "—"

        stroki_tablitsy.append(
            (
                m.kod,
                m.nazvanie,
                str(m.nominal),
                formatirovat_chislo_ru(m.znachenie, 4),
                izmenenie,
            )
        )

    zagolovok = "**Официальные курсы валют ЦБ РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Код", "Валюта", "Номинал", "Курс (₽)", "Изменение"],
        stroki_tablitsy,
    )


async def uznat_kurs_valyuty(kod: str, ctx: Context) -> str:
    """Получить курс одной конкретной валюты ЦБ РФ.

    Доступные коды: USD, EUR, CNY, GBP, JPY, CHF, KZT, BYN и др.
    Используйте spisok_valyut() для полного списка.

    Аргументы:
        kod: Код валюты (например, 'USD', 'EUR', 'CNY').

    Возвращает:
        Подробная информация о курсе валюты.
    """
    await ctx.info(f"Запрос курса {kod}...")
    valyuta = await client.poluchit_valyutu(kod)

    if not valyuta:
        return (
            f"Валюта '{kod}' не найдена в справочнике ЦБ РФ.\n\n"
            f"Попробуйте один из основных: USD, EUR, CNY, GBP, JPY, CHF"
        )

    stroki = [
        f"**{valyuta.nazvanie}** ({valyuta.kod})",
        f"- Номинал: {valyuta.nominal}",
        f"- Курс: {formatirovat_chislo_ru(valyuta.znachenie, 4)} ₽",
    ]

    if valyuta.predydushchee_znachenie is not None:
        raznitsa = valyuta.znachenie - valyuta.predydushchee_znachenie
        znak = "+" if raznitsa >= 0 else ""
        predydushchee = valyuta.predydushchee_znachenie
        protsent = (raznitsa / predydushchee) * 100 if predydushchee else 0
        predydushchaya_stroka = formatirovat_chislo_ru(valyuta.predydushchee_znachenie, 4)
        stroki.append(f"- Предыдущий: {predydushchaya_stroka} ₽")
        protsent_str = f"{znak}{formatirovat_chislo_ru(protsent, 2)}%"
        raznitsa_str = f"{znak}{formatirovat_chislo_ru(raznitsa, 4)}"
        stroki.append(f"- Изменение: {raznitsa_str} ({protsent_str})")

    if valyuta.data:
        stroki.append(f"- Дата: {valyuta.data}")

    stroki.append("- Источник: Центральный банк Российской Федерации")
    return "\n".join(stroki)


async def spisok_valyut(ctx: Context) -> str:
    """Получить полный список валют, доступных в справочнике ЦБ РФ.

    Возвращает:
        Список всех доступных валют с кодами и названиями.
    """
    await ctx.info("Запрос списка валют ЦБ РФ...")
    rezultat = await client.poluchit_vse_valyuty()
    dannye_valyut = rezultat.get("Valute", {})

    stroki_tablitsy = []
    for kod, zapis in sorted(dannye_valyut.items()):
        nazvanie_valyuty = zapis.get("Name", kod)
        nominal_valyuty = zapis.get("Nominal", 1)
        znachenie_kursa = zapis.get("Value", 0)
        znachenie_za_edinitsu = (
            znachenie_kursa / nominal_valyuty if nominal_valyuty else znachenie_kursa
        )
        stroki_tablitsy.append(
            (
                kod,
                nazvanie_valyuty,
                str(nominal_valyuty),
                formatirovat_chislo_ru(znachenie_za_edinitsu, 4),
            )
        )

    zagolovok = f"**Справочник валют ЦБ РФ** — {len(stroki_tablitsy)} валют\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Код", "Валюта", "Номинал", "Курс (₽)"],
        stroki_tablitsy,
    )


async def konvertirovat_valyutu(
    valyuta: str,
    kolichestvo: float,
    ctx: Context,
) -> str:
    """Конвертировать сумму из иностранной валюты в рубли по курсу ЦБ РФ.

    Аргументы:
        valyuta: Код валюты (USD, EUR, CNY и т.д.).
        kolichestvo: Сумма в иностранной валюте.

    Возвращает:
        Результат конвертации.
    """
    await ctx.info(f"Конвертация {kolichestvo} {valyuta} в рубли...")
    dannye = await client.poluchit_valyutu(valyuta)

    if not dannye:
        return f"Валюта '{valyuta}' не найдена в справочнике ЦБ РФ."

    rubli = dannye.znachenie * kolichestvo

    stroki = [
        "**Конвертация валюты**",
        f"- Сумма: {formatirovat_chislo_ru(kolichestvo, 2)} {dannye.kod} ({dannye.nazvanie})",
        f"- Курс ЦБ РФ: {formatirovat_chislo_ru(dannye.znachenie, 4)} ₽ за 1 {dannye.kod}",
        f"- Номинал: {dannye.nominal}",
        f"- **Результат: {formatirovat_chislo_ru(rubli, 2)} ₽**",
    ]

    if dannye.data:
        stroki.append(f"- Дата курса: {dannye.data}")

    return "\n".join(stroki)


async def sravnit_valyuty(kody: list[str] | None = None, ctx: Context | None = None) -> str:
    """Сравнить курсы нескольких валют ЦБ РФ.

    Аргументы:
        kody: Коды валют для сравнения (например, ['USD', 'EUR', 'CNY']).
              По умолчанию сравниваются USD, EUR, CNY.

    Возвращает:
        Сравнительная таблица курсов.
    """
    if not kody:
        kody = ["USD", "EUR", "CNY"]

    if len(kody) > 10:
        return "Можно сравнить не более 10 валют одновременно."

    if ctx is not None:
        await ctx.info(f"Сравнение {len(kody)} валют...")
    valyuty = await client.poluchit_valyuty_spisok(kody)

    if not valyuty:
        return "Не удалось получить данные для указанных валют."

    stroki_tablitsy = []
    for m in sorted(valyuty, key=lambda x: x.kod):
        izmenenie = "—"
        if m.predydushchee_znachenie is not None and m.predydushchee_znachenie > 0:
            raznitsa = m.znachenie - m.predydushchee_znachenie
            protsent = (raznitsa / m.predydushchee_znachenie) * 100
            znak = "+" if protsent >= 0 else ""
            izmenenie = f"{znak}{formatirovat_chislo_ru(protsent, 2)}%"
        stroki_tablitsy.append(
            (m.kod, m.nazvanie, formatirovat_chislo_ru(m.znachenie, 4), izmenenie)
        )

    zagolovok = "**Сравнение курсов валют ЦБ РФ**\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Код", "Валюта", "Курс (₽)", "Изменение"],
        stroki_tablitsy,
    )


async def kursy_po_stranam(ctx: Context) -> str:
    """Получить курсы валют для основных стран-партнёров России.

    Возвращает:
        Таблица с курсами валют по странам.
    """
    await ctx.info("Запрос курсов валют по странам...")
    valyuty = await client.poluchit_valyuty_spisok(list(VALYUTY_PO_STRANAM.values()))

    if not valyuty:
        return "Не удалось получить данные."

    stroki_tablitsy = []
    for m in sorted(valyuty, key=lambda x: x.kod):
        strana = next((p for p, c in VALYUTY_PO_STRANAM.items() if c == m.kod), m.kod)
        stroki_tablitsy.append((strana, m.kod, formatirovat_chislo_ru(m.znachenie, 4)))

    zagolovok = "**Курсы валют основных стран-партнёров России**\n\n"
    return zagolovok + tablitsa_v_markdown(
        ["Страна", "Код", "Курс (₽)"],
        stroki_tablitsy,
    )
