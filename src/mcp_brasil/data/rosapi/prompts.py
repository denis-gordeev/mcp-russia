"""Prompts for the RosAPI feature."""

from __future__ import annotations

import mcp.types as mt
from fastmcp.prompts import Message, PromptMessage, PromptResult


def analiz_organizacii(inn: str) -> PromptResult:
    """Подсказка для анализа организации по ИНН.

    Args:
        inn: ИНН организации для проверки.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            f"Проведи анализ организации по ИНН {inn}.\n\n"
                            f"Используй следующие шаги:\n"
                            f"1. Найди организацию через poisk_org_po_inn\n"
                            f"2. Проверь её статус (действующая/ликвидирована)\n"
                            f"3. Определи регион регистрации\n"
                            f"4. Сообщи основную информацию\n\n"
                            f"Если организация не найдена, сообщи об этом "
                            f"и предложи проверить корректность ИНН."
                        ),
                    ),
                )
            )
        ]
    )


def poisk_adresa_prompt(adres: str) -> PromptResult:
    """Подсказка для поиска адреса через ФИАС.

    Args:
        adres: Адрес для поиска.
    """
    return PromptResult(
        messages=[
            Message(
                PromptMessage(
                    role="user",
                    content=mt.TextContent(
                        type="text",
                        text=(
                            f"Найди адрес через ФИАС: {adres}\n\n"
                            f"Используй poisk_adresa для поиска.\n"
                            f"Если найдено несколько вариантов, покажи топ-3 "
                            f"и спроси, какой подходит пользователю.\n\n"
                            f"Если адрес не найден, предложи уточнить запрос."
                        ),
                    ),
                )
            )
        ]
    )
