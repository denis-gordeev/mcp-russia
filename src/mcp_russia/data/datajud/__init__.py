"""⚠️ DEPRECATED — Legacy feature DataJud — переходный слой судебных данных Бразилии.

.. deprecated::
    Используйте модуль ``mcp_russia.data.kad_arbitrazh`` (КАД — kad.arbitr.ru) для российских арбитражных дел.
    Данный модуль сохраняет обратную совместимость для бразильских DataJud/CNJ интеграций.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="datajud",
    description=(
        "⚠️ DEPRECATED — Legacy-слой DataJud (CNJ) внутри mcp-russia: "
        "бразильские судебные процессы, движения дел и справочники tribunais. "
        "Для российских арбитражных дел используйте модуль kad_arbitrazh (КАД)."
    ),
    version="0.1.0-deprecated",
    api_base="https://api-publica.datajud.cnj.jus.br",
    requires_auth=True,
    auth_env_var="DATAJUD_API_KEY",
    tags=[
        "⚠️ DEPRECATED",
        "judiciario",
        "processos",
        "cnj",
        "tribunais",
        "datajud",
        "бразилия-legacy",
    ],
)
