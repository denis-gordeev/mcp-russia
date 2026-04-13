"""⚠️ DEPRECATED — Legacy-слой INPE внутри mcp-russia — Instituto Nacional de Pesquisas Espaciais (compatibility layer, legacy).

.. deprecated::
    Используйте будущие модули Росгидромета и Росприроднадзора
    для российских экологических и метеорологических данных.
    Данный модуль сохраняет обратную совместимость для бразильских данных INPE.
"""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="inpe",
    description=(
        "⚠️ DEPRECATED — Legacy-слой INPE внутри mcp-russia: "
        "Национальный институт космических исследований Бразилии: очаги пожаров, "
        "оповещения о вырубке DETER, исторические данные PRODES и спутники. "
        "Для российских экологических данных используйте будущие модули Росгидромета/Росприроднадзора."
    ),
    version="0.1.0-deprecated",
    api_base="https://terrabrasilis.dpi.inpe.br",
    requires_auth=False,
    tags=["⚠️ DEPRECATED", "пожары", "вырубка-лесов", "амазония", "окружающая-среда", "inpe", "бразилия-legacy"],
)
