"""⚠️ DEPRECATED — Legacy-слой ANA внутри mcp-russia — Agência Nacional de Águas (compatibility layer, legacy).

.. deprecated::
    Используйте будущие модули Росводресурсов и Росгидромета
    для российских гидрологических данных.
    Данный модуль сохраняет обратную совместимость для бразильских данных ANA.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="ana",
    description=(
        "⚠️ DEPRECATED — Legacy-слой ANA внутри mcp-russia: "
        "Национальное агентство водных ресурсов Бразилии: гидрологические станции, "
        "телеметрия расхода воды и мониторинг водохранилищ. "
        "Для российских гидрологических данных используйте будущие модули Росводресурсов/Росгидромета."
    ),
    version="0.1.0-deprecated",
    api_base="https://www.snirh.gov.br/hidroweb/rest/api",
    requires_auth=False,
    tags=[
        "⚠️ DEPRECATED",
        "agua",
        "hidrologia",
        "reservatorios",
        "rios",
        "chuva",
        "бразилия-legacy",
    ],
    enabled=False,
)
