"""Переходный слой судебного поиска по бразильским высшим судам."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="jurisprudencia",
    description=(
        "Переходный judicial-layer: поиск решений, обзоров и суммул "
        "по STF, STJ и TST как legacy-совместимому источнику."
    ),
    version="0.1.0",
    api_base="https://jurisprudencia.stf.jus.br",
    requires_auth=False,
    tags=["judiciario", "jurisprudencia", "stf", "stj", "tst", "sumulas"],
)
