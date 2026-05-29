"""Prompts for the INPE feature — analysis templates for LLMs.

NOTE: This is a legacy/compatibility layer within mcp-russia.
These Brazilian environmental monitoring prompts are kept for backward
compatibility with the historical INPE integration and are NOT part of the
target Russian data model.

Prompts provide reusable message templates that guide LLM interactions.
They appear in client UIs (e.g., Claude Desktop) as slash-commands.
"""

from __future__ import annotations


def monitoramento_ambiental(regiao: str = "Amazônia") -> str:
    """Генерирует анализ экологического мониторинга региона (legacy — Бразилия).

    Cria um template que orienta o LLM a consultar dados de queimadas,
    desmatamento e alertas DETER para uma região específica.

    Args:
        regiao: Nome da região ou bioma a analisar (ex: Amazônia, Cerrado, PA).
    """
    return (
        f"Выполни полный анализ экологического мониторинга региона: {regiao}.\n\n"
        "Контекст:\n"
        "- Репозиторий `mcp-russia` всё ещё находится в миграции.\n"
        "- Данные поступают из исторического бразильского integration-layer\n"
        "  (INPE — Национальный институт космических исследований, Бразилия).\n\n"
        "Рекомендуемые шаги:\n"
        "1. Use dados_satelite() para listar os satélites de monitoramento disponíveis\n"
        f"2. Use buscar_focos_queimadas(estado ou bioma relacionado a '{regiao}') "
        "para obter focos de incêndio recentes\n"
        f"3. Use alertas_deter(bioma ou estado relacionado a '{regiao}') "
        "para verificar alertas de desmatamento\n"
        f"4. Use consultar_desmatamento(bioma ou estado relacionado a '{regiao}') "
        "para dados históricos do PRODES\n\n"
        "Сформируй отчёт:\n"
        "- Резюме текущей ситуации (очаги пожаров и свежие оповещения)\n"
        "- Историческая динамика вырубки лесов в регионе\n"
        "- Основные затронутые муниципалитеты\n"
        "- Сравнение по биомам (если применимо)\n"
        "- Рекомендации по мониторингу\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )
