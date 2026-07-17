"""Инструменты для создания официальных документов РФ.

Основано на ГОСТ Р 7.0.97-2016 и правилах делопроизводства РФ.

Правила (ADR-001):
    - Возвращает форматированные строки для использования LLM
"""

from __future__ import annotations

import re
from datetime import datetime

from .constants import (
    МЕСЯЦЫ,
    ОБРАЩЕНИЯ,
    ПРЕФИКСЫ_ДОКУМЕНТОВ,
)


async def formatirovat_datu_propisyu(
    gorod: str = "Москва",
) -> str:
    """Форматирует текущую дату по стандартам официальных документов РФ.

    Согласно ГОСТ Р 7.0.97-2016: название города, день (1-е число —
    порядковое, остальные — количественное), месяц в родительном падеже,
    год, точка в конце.

    Аргументы:
        gorod: Название города. По умолчанию: Москва.

    Возвращает:
        Дата в формате: «г. Москва, 15 марта 2026 г.»
    """
    segodnya = datetime.now()
    mesyac = МЕСЯЦЫ[segodnya.month]
    den = "1" if segodnya.day == 1 else str(segodnya.day)
    return f"г. {gorod}, {den} {mesyac} {segodnya.year} г."


async def generirovat_numeraciyu(
    tip: str,
    nomer: int,
    god: int | None = None,
    otdel: str = "",
) -> str:
    """Генерирует номер официального документа.

    Стандартный формат: ТИП № НОМЕР/ГОД/ОТДЕЛ

    Аргументы:
        tip: Тип документа (письмо, распоряжение, приказ, акт, справка,
             протокол, докладная_записка).
        nomer: Порядковый номер документа.
        god: Год документа (по умолчанию — текущий).
        otdel: Аббревиатура подразделения. Необязательно.

    Возвращает:
        Номер документа (например, «ПИСЬМО № 42/2026/Д-15»).
    """
    god = god or datetime.now().year
    tip = tip.lower().strip()

    prefiks = ПРЕФИКСЫ_ДОКУМЕНТОВ.get(tip, tip.upper())

    if otdel:
        return f"{prefiks} № {nomer}/{god}/{otdel}"
    return f"{prefiks} № {nomer}/{god}"


async def konsulitirovat_obrashchenie(dolzhnost: str) -> str:
    """Возвращает правильную форму обращения к должностному лицу.

    Основано на правилах российского делопроизводства.

    Аргументы:
        dolzhnost: Должность адресата (например, «Министр», «Губернатор»).

    Возвращает:
        Форма обращения, титулование и адресация.
    """
    dolzhnost_lower = dolzhnost.lower().strip()

    # Точный поиск
    if dolzhnost_lower in ОБРАЩЕНИЯ:
        o = ОБРАЩЕНИЯ[dolzhnost_lower]
        return (
            f"Должность: {dolzhnost}\n"
            f"Обращение: {o['обращение']}\n"
            f"Титулование: {o['титулование']}\n"
            f"Адресация: {o['адресация']}"
        )

    # Частичный поиск
    for klyuch, obrashcheniye in ОБРАЩЕНИЯ.items():
        if klyuch in dolzhnost_lower or dolzhnost_lower in klyuch:
            return (
                f"Должность: {dolzhnost} (похоже на: {klyuch})\n"
                f"Обращение: {obrashcheniye['обращение']}\n"
                f"Титулование: {obrashcheniye['титулование']}\n"
                f"Адресация: {obrashcheniye['адресация']}"
            )

    # По умолчанию
    return (
        f"Должность: {dolzhnost}\n"
        f"Обращение: Уважаемый господин/госпожа {dolzhnost}\n"
        f"Титулование: {dolzhnost} [наименование организации]\n"
        f"Адресация: [Должность] [наименование организации]"
    )


async def validirovat_dokument(tekst: str, tip: str) -> str:
    """Проверяет документ на соответствие нормам делопроизводства.

    Проверяет формальные аспекты: дата, номер, подписи, стиль.

    Аргументы:
        tekst: Текст документа.
        tip: Тип документа (письмо, приказ, распоряжение, акт, справка,
             протокол, докладная_записка).

    Возвращает:
        Отчёт о валидации с проблемами и рекомендациями.
    """
    problemy: list[str] = []
    rekomendacii: list[str] = []

    # Проверка даты
    mesyacy_spisok = list(МЕСЯЦЫ.values())
    est_data = any(mesyac in tekst.lower() for mesyac in mesyacy_spisok)
    if not est_data:
        problemy.append("Отсутствует дата в документе")

    # Проверка номера
    est_nomer = "№" in tekst or "номер" in tekst.lower()
    if not est_nomer and tip in ("письмо", "приказ", "распоряжение", "акт", "протокол"):
        rekomendacii.append("Рекомендуется указать номер документа")

    # Проверка подписи
    if tip in ("письмо", "приказ", "распоряжение", "акт", "справка") and "__________" not in tekst:
        rekomendacii.append("Отсутствует место для подписи")

    # Проверка на излишне эмоциональные выражения
    izbytochnye = [
        "с наилучшими пожеланиями",
        "искренне ваш",
        "до свидания",
        "с благодарностью",
    ]
    for fraza in izbytochnye:
        if fraza in tekst.lower():
            rekomendacii.append(f"Фраза «{fraza}» не соответствует официальному стилю")

    # Проверка на герундий (деепричастия)
    deeprichastiya = re.findall(r"\b\w+(?:я|ая|учи|в)\b", tekst)
    if len(deeprichastiya) > 5:
        rekomendacii.append(
            f"Найдено {len(deeprichastiya)} деепричастий — "
            "официальный стиль предпочитает прямые формы"
        )

    # Проверка длинных абзацев
    abzaczy = [abzats for abzats in tekst.split("\n\n") if abzats.strip()]
    dlinnye = [abzats for abzats in abzaczy if len(abzats) > 500]
    if dlinnye:
        rekomendacii.append(
            f"{len(dlinnye)} абзац(ев) длиннее 500 символов — рекомендуется разделить для ясности"
        )

    # Отчёт
    if not problemy and not rekomendacii:
        return "Документ соответствует нормам делопроизводства. Проблем не обнаружено."

    otchet = "ОТЧЁТ О ВАЛИДАЦИИ ДОКУМЕНТА\n\n"
    if problemy:
        otchet += "Обнаружены проблемы:\n"
        otchet += "\n".join(f"  - {problema}" for problema in problemy)
        otchet += "\n\n"
    if rekomendacii:
        otchet += "Рекомендации по улучшению:\n"
        otchet += "\n".join(f"  - {rekomendatsiya}" for rekomendatsiya in rekomendacii)

    return otchet


async def spisok_tipov_dokumentov() -> str:
    """Возвращает список поддерживаемых типов официальных документов.

    Возвращает:
        Форматированный список типов с описанием.
    """
    tipy = {
        "письмо": "Официальная переписка с внешними организациями",
        "распоряжение": "Акт по оперативным вопросам деятельности",
        "приказ": "Правовой акт руководителя организации",
        "акт": "Документ, фиксирующий факты и события",
        "справка": "Документ с фактическими данными",
        "протокол": "Запись хода заседания коллегиального органа",
        "докладная_записка": "Документ внутреннего обращения к руководителю",
    }

    stroki = ["Поддерживаемые типы официальных документов:\n"]
    for tip, opisanie in tipy.items():
        stroki.append(f"  - {tip}: {opisanie}")

    stroki.append(
        "\nИспользуйте инструменты deloproizvodstvo для создания каждого типа. "
        "Шаблоны доступны в shablony/."
    )
    return "\n".join(stroki)
