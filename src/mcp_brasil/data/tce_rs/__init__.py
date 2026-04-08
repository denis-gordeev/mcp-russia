"""Legacy-слой TCE-RS внутри mcp-russia — Tribunal de Contas do Rio
Grande do Sul (compatibility layer)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tce_rs",
    description=(
        "Legacy-слой TCE-RS внутри mcp-russia: "
        "Индексы образования и здравоохранения, фискальное управление (LRF) "
        "и каталог данных муниципалитетов Риу-Гранди-ду-Сул "
        "через портал CKAN TCE-RS."
    ),
    version="0.1.0",
    api_base="https://dados.tce.rs.gov.br",
    requires_auth=False,
    tags=["tce", "rs", "educacao", "saude", "gestao-fiscal", "ckan"],
)
