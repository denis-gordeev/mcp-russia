"""⚠️ DEPRECATED — Legacy-слой TransfereGov внутри mcp-russia — parliamentary amendments pix (compatibility layer, legacy).

.. deprecated::
    Используйте модуль ``mcp_russia.data.gosduma`` (Госдума) и будущий модуль Минфина РФ
    для российских бюджетных данных.
    Данный модуль сохраняет обратную совместимость для бразильских данных TransfereGov.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="transferegov",
    description=(
        "⚠️ DEPRECATED — Legacy-слой TransfereGov внутри mcp-russia — "
        "парламентские поправки pix (специальные трансферты): "
        "поиск по автору, муниципалитету, году и детализации. "
        "Для российских бюджетных данных используйте модуль gosduma."
    ),
    version="0.1.0-deprecated",
    api_base="https://api.transferegov.gestao.gov.br",
    requires_auth=False,
    tags=[
        "⚠️ DEPRECATED",
        "emendas",
        "pix",
        "transferencias",
        "parlamentar",
        "municipio",
        "бразилия-legacy",
    ],
)
