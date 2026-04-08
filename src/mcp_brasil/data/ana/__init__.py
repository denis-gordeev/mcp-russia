"""Legacy-слой ANA внутри mcp-russia — Agência Nacional de Águas (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="ana",
    description=(
        "Legacy-слой ANA внутри mcp-russia: "
        "Национальное агентство водных ресурсов Бразилии: гидрологические станции, "
        "телеметрия расхода воды и мониторинг водохранилищ."
    ),
    version="0.1.0",
    api_base="https://www.snirh.gov.br/hidroweb/rest/api",
    requires_auth=False,
    tags=["agua", "hidrologia", "reservatorios", "rios", "chuva"],
)
