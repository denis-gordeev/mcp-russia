"""ГИБДД/МВД — данные Госавтоинспекции и Министерства внутренних дел."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="gibdd",
    description=(
        "Данные ГИБДД/МВД России: штрафы, проверка транспортных средств, "
        "водительских удостоверений, статистика ДТП, регистрационные действия"
    ),
    version="0.1.0",
    api_base="https://гибдд.рф",
    requires_auth=False,
    tags=["гибдд", "мвд", "штрафы", "транспорт", "дтп", "водители"],
)
