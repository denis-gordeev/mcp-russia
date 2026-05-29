"""⚠️ DEPRECATED — Legacy-слой Diário Oficial внутри mcp-russia — поиск в официальных муниципальных газетах через Querido Diário (compatibility layer, legacy).

.. deprecated::
    Используйте будущий модуль официальных публикаций РФ (pravo.gov.ru, consultant.ru)
    для российских официальных документов.
    Данный модуль сохраняет обратную совместимость для бразильских данных Querido Diário.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="diario_oficial",
    description=(
        "⚠️ DEPRECATED — Legacy-слой Querido Diário внутри mcp-russia: "
        "Текстовый поиск в официальных муниципальных газетах 5000+ городов Бразилии. "
        "Контракты, назначения, санкции, тендеры и административные акты. "
        "Для российских официальных документов используйте будущие модули pravo.gov.ru/consultant.ru."
    ),
    version="0.1.0-deprecated",
    api_base="https://queridodiario.ok.org.br",
    requires_auth=False,
    tags=[
        "⚠️ DEPRECATED",
        "официальная-газета",
        "прозрачность",
        "муниципалитеты",
        "тендеры",
        "контракты",
        "бразилия-legacy",
    ],
)
