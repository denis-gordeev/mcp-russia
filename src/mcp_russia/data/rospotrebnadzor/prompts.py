"""Промпты модуля Роспотребнадзора.

Все промпты на русском с пометками «(заглушка)», так как
это модуль-заглушка в ожидании реальной интеграции с API.
"""

from __future__ import annotations

import mcp.types as mt
from fastmcp.prompts import Message, PromptMessage, PromptResult


def analiz_proverki() -> PromptResult:
    """Анализ результатов проверки. (заглушка)

    Используйте этот промпт для анализа результатов проверки объекта надзора.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Выполните анализ результатов проверки:\n\n"
                            "1. Определите тип и цель проверки.\n"
                            "2. Оцените количество и характер выявленных нарушений.\n"
                            "3. Укажите ссылки на нарушенные нормативные акты (СанПиН).\n"
                            "4. Оцените серьёзность нарушений и рекомендации.\n"
                            "5. Предложите меры по устранению нарушений.\n\n"
                            "Используйте tools: spisok_tipov_proverok, info_proverki, "
                            "poisk_narusheniy, spisok_sanpinov."
                        ),
                    ),
                )
            )
        ]
    )


def obzor_sanitarnoy_situacii() -> PromptResult:
    """Обзор санитарно-эпидемиологической ситуации в регионе. (заглушка)

    Используйте этот промпт для обзора санитарной ситуации.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Подготовьте обзор санитарно-эпидемиологической ситуации:\n\n"
                            "1. Охарактеризуйте основные показатели безопасности.\n"
                            "2. Оцените тенденции по ключевым направлениям.\n"
                            "3. Сравните с предельно допустимыми значениями.\n"
                            "4. Укажите проблемные области.\n"
                            "5. Предложите меры по улучшению.\n\n"
                            "Используйте tools: pokazateli_bezopasnosti, "
                            "poisk_narusheniy, zhaloby_potrebiteley, "
                            "spisok_kategoriy_obiektov."
                        ),
                    ),
                )
            )
        ]
    )
