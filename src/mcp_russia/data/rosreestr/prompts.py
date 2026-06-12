"""Промпты модуля Росреестра.

Все промпты на русском с пометками «(legacy — placeholder)», так как
это модуль-заглушка в ожидании реальной интеграции с API.
"""

from __future__ import annotations

import mcp.types as mt
from fastmcp.prompts import Message, PromptMessage, PromptResult


def analiz_nedvizhimosti() -> PromptResult:
    """Анализ объекта недвижимости по кадастровому номеру. (legacy — placeholder)

    Используйте этот промпт для анализа объекта недвижимости.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Выполните анализ объекта недвижимости:\n\n"
                            "1. Получите сведения об объекте по кадастровому номеру.\n"
                            "2. Определите тип объекта и категорию земель.\n"
                            "3. Проверьте кадастровую стоимость и дату определения.\n"
                            "4. Уточните статус учёта и зарегистрированные права.\n"
                            "5. Оцените рыночную стоимость относительно кадастровой.\n\n"
                            "Используйте tools: info_obekta, kadastrovaya_stoimost, "
                            "prava_na_obekt, spisok_kategoriy_zemel."
                        ),
                    ),
                )
            )
        ]
    )


def obzor_zemelnogo_uchastka() -> PromptResult:
    """Обзор земельного участка для покупки или использования. (legacy — placeholder)

    Используйте этот промпт для оценки земельного участка.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Подготовьте обзор земельного участка:\n\n"
                            "1. Получите кадастровые сведения об участке.\n"
                            "2. Определите категорию земель и вид разрешённого использования.\n"
                            "3. Проверьте кадастровую стоимость.\n"
                            "4. Уточните форму собственности и обременения.\n"
                            "5. Оцените возможности использования участка.\n\n"
                            "Используйте tools: info_obekta, kadastrovaya_stoimost, "
                            "spisok_kategoriy_zemel, spisok_vidov_ispolzovaniya, "
                            "prava_na_obekt."
                        ),
                    ),
                )
            )
        ]
    )
