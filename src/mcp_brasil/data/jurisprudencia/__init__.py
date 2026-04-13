"""⚠️ DEPRECATED — Legacy-слой Jurisprudencia внутри mcp-russia — судебные решения бразильских высших судов (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_brasil.data.kad_arbitrazh`` (КАД — kad.arbitr.ru)
    для российских судебных данных.
    Данный модуль сохраняет обратную совместимость для бразильских данных STF/STJ/TST.
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="jurisprudencia",
    description=(
        "⚠️ DEPRECATED — Legacy-слой Jurisprudencia внутри mcp-russia: "
        "Поиск решений, обзоров и суммул по STF, STJ и TST. "
        "Для российских судебных данных используйте модуль kad_arbitrazh."
    ),
    version="0.1.0-deprecated",
    api_base="https://jurisprudencia.stf.jus.br",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "judiciario", "jurisprudencia", "stf", "stj", "tst", "sumulas", "бразилия-legacy"],
)
