"""Промпты модуля Роскомнадзора.

Все промпты на русском с пометками «(legacy)», так как
это модуль-заглушка в ожидании реальной интеграции с API.
"""

from __future__ import annotations

import mcp.types as mt
from fastmcp.prompts import Message, PromptMessage, PromptResult


def analiz_narusheniya() -> PromptResult:
    """Анализ нарушения в сфере связи/ИТ. (legacy — placeholder)

    Используйте этот промпт для анализа нарушений, выявленных Роскомнадзором.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Выполните анализ нарушения в сфере связи/ИТ:\n\n"
                            "1. Определите тип и категорию нарушения.\n"
                            "2. Укажите нарушенные нормативные акты (149-ФЗ, 152-ФЗ и т.д.).\n"
                            "3. Оцените масштаб и последствия нарушения.\n"
                            "4. Определите меры ответственности и штрафы.\n"
                            "5. Предложите рекомендации по устранению.\n\n"
                            "Используйте tools: spisok_kategoriy_narusheniy, "
                            "poisk_narusheniy, spisok_reestrov, zapisi_reestra."
                        ),
                    ),
                )
            )
        ]
    )


def obzor_reestrov() -> PromptResult:
    """Обзор реестров Роскомнадзора. (legacy — placeholder)

    Используйте этот промпт для обзора реестров и структуры данных Роскомнадзора.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            "Подготовьте обзор реестров Роскомнадзора:\n\n"
                            "1. Перечислите основные реестры и их назначение.\n"
                            "2. Охарактеризуйте порядок ведения каждого реестра.\n"
                            "3. Укажите правовые основания ведения реестров.\n"
                            "4. Опишите процедуры включения и исключения записей.\n"
                            "5. Оцените доступность данных для публичного использования.\n\n"
                            "Используйте tools: spisok_reestrov, zapisi_reestra, "
                            "spisok_napravleniy, spisok_kategoriy_narusheniy."
                        ),
                    ),
                )
            )
        ]
    )
