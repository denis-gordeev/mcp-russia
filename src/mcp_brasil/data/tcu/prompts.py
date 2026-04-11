"""Analysis prompts for the TCU feature.

NOTE: This is a legacy/compatibility layer within mcp-russia.
These Brazilian federal audit court analysis prompts are kept for backward
compatibility with the historical TCU (Tribunal de Contas da União) integration
and are NOT part of the target Russian data model.
"""

from __future__ import annotations


def investigar_empresa_tcu(cnpj: str) -> str:
    """Полное расследование компании в реестрах Счётного суда (legacy — Бразилия).

    Verifica a situação de uma empresa em todos os cadastros de
    sanções do TCU, incluindo inidoneidade, certidões consolidadas
    e contratos com o tribunal.

    Args:
        cnpj: CNPJ da empresa (somente números, 14 dígitos).
    """
    return (
        f"Исследуй компанию с CNPJ {cnpj} в реестрах TCU.\n\n"
        "Контекст:\n"
        "- Репозиторий `mcp-russia` всё ещё находится в миграции.\n"
        "- Данные поступают из исторического бразильского integration-layer\n"
        "  (TCU — Tribunal de Contas da União, Счётный суд Бразилии).\n\n"
        "1. Use `consultar_certidoes_apf` para verificar a situação "
        "consolidada em 4 cadastros (TCU Inidôneos, CNJ CNIA, CGU CEIS, CGU CNEP)\n"
        "2. Use `consultar_inidoneos` com o CNPJ para verificar se a empresa "
        "está na lista de licitantes inidôneos\n"
        "3. Подготовь ясное резюме ситуации компании:\n"
        "   - Наличие ограничений в каком-либо реестре\n"
        "   - Детали найденных санкций\n"
        "   - Имеет ли компания право участвовать в госзакупках\n\n"
        "Пометка: это legacy-бразильский источник в переходном контуре `mcp-russia`."
    )
