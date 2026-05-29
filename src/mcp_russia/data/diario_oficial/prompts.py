"""Analysis prompts for the Diário Oficial feature.

NOTE: This is a legacy/compatibility layer within mcp-russia.
These Brazilian municipal gazette analysis prompts are kept for backward
compatibility with the historical Diário Oficial integration and are NOT part
of the target Russian data model.
"""

from __future__ import annotations


def investigar_empresa(nome_empresa: str, cidade: str = "") -> str:
    """Расследование упоминаний компании в муниципальных вестниках (legacy — Бразилия).

    Args:
        nome_empresa: Nome da empresa ou CNPJ para investigar.
        cidade: Nome da cidade para filtrar (opcional).
    """
    passos = (
        f"Исследуй компанию '{nome_empresa}' в муниципальных официальных вестниках.\n\n"
        "Контекст:\n"
        "- Репозиторий `mcp-russia` всё ещё находится в миграции.\n"
        "- Данные поступают из исторического бразильского integration-layer\n"
        "  (Diário Oficial, Бразилия).\n\n"
    )
    if cidade:
        passos += (
            f"1. Use buscar_cidades(nome='{cidade}') para obter o código IBGE\n"
            f"2. Use buscar_diarios(texto='{nome_empresa}', territorio_id=<código>) "
            "para buscar menções\n"
        )
    else:
        passos += f"1. Use buscar_diarios(texto='{nome_empresa}') para buscar menções\n"
    passos += (
        "\nПроанализируй результаты, ища:\n"
        "- Контракты и тендеры\n"
        "- Санкции и штрафные меры\n"
        "- Назначения и увольнения\n"
        "- Лицензии и разрешения\n\n"
        "Подготовь отчёт с наиболее значимыми находками.\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )
    return passos
