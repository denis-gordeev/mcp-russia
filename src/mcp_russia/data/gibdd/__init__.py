"""ГИБДД/МВД — данные Госавтоинспекции и Министерства внутренних дел."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    name="gibdd",
    description=(
        "Данные ГИБДД/МВД России: штрафы, проверка транспортных средств, "
        "водительских удостоверений, статистика ДТП, регистрационные действия"
    ),
    version="0.2.0",
    api_base="https://гибдд.рф",
    requires_auth=False,
    tags=["гибдд", "мвд", "штрафы", "транспорт", "дтп", "водители"],
)
