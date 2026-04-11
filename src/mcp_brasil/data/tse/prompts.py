"""Prompts for the TSE feature — analysis templates for LLMs.

NOTE: This is a legacy/compatibility layer within mcp-russia.
These Brazilian electoral analysis prompts are kept for backward compatibility
with the historical TSE (Tribunal Superior Eleitoral) integration and are NOT
part of the target Russian data model.
"""

from __future__ import annotations


def analise_candidato(
    nome: str,
    ano: int,
    municipio: int,
    eleicao_id: int,
    cargo: int,
) -> str:
    """Генерирует полный анализ кандидата (legacy — Бразилия).

    Orienta o LLM a consultar dados do candidato, patrimônio e prestação de contas.

    Args:
        nome: Nome do candidato para buscar.
        ano: Ano da eleição.
        municipio: Código do município.
        eleicao_id: ID da eleição.
        cargo: Código do cargo.
    """
    return (
        f"Подготовь полный анализ кандидата '{nome}' "
        f"на выборах {ano} года.\n\n"
        "Контекст:\n"
        "- Репозиторий `mcp-russia` всё ещё находится в миграции.\n"
        "- Данные поступают из исторического бразильского integration-layer\n"
        "  (TSE — Верховный избирательный суд, Бразилия).\n\n"
        "Passos:\n"
        f"1. Use listar_candidatos(ano={ano}, municipio={municipio}, "
        f"eleicao_id={eleicao_id}, cargo={cargo}) para encontrar o candidato\n"
        "2. Com o ID do candidato, use buscar_candidato() para detalhes completos\n"
        "3. Use consultar_prestacao_contas() para ver as finanças de campanha\n\n"
        "Сформируй отчёт:\n"
        "- Персональные и избирательные данные\n"
        "- Декларированное имущество (общая стоимость)\n"
        "- Доходы и расходы кампании\n"
        "- Основные спонсоры и поставщики\n"
        "- Статус кандидатуры (допущен/не допущен, чистая ли справка)\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )


def comparativo_eleicao(ano: int, municipio: int, eleicao_id: int, cargo: int) -> str:
    """Генерирует сравнительный анализ кандидатов выборов (legacy — Бразилия).

    Args:
        ano: Ano da eleição.
        municipio: Código do município.
        eleicao_id: ID da eleição.
        cargo: Código do cargo.
    """
    return (
        f"Сравни кандидатов на выборах {ano} года.\n\n"
        "Контекст:\n"
        "- Данные поступают из исторического бразильского слоя TSE.\n\n"
        "Passos:\n"
        f"1. Use listar_candidatos(ano={ano}, municipio={municipio}, "
        f"eleicao_id={eleicao_id}, cargo={cargo})\n"
        "2. Para cada candidato, use buscar_candidato() para detalhes\n"
        "3. Para cada candidato, use consultar_prestacao_contas()\n\n"
        "Подготовь сравнительную таблицу:\n"
        "- Имя, партия, номер\n"
        "- Декларированное имущество\n"
        "- Доходы и расходы кампании\n"
        "- Статус (допущен/не допущен)\n"
        "- Образование и род занятий\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )
