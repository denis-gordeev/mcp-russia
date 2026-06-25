"""ГИБДД/МВД — данные Госавтоинспекции и Министерства внутренних дел."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="gibdd",
    opisanie=(
        "Данные ГИБДД/МВД России: штрафы, проверка транспортных средств, "
        "водительских удостоверений, статистика ДТП, регистрационные действия"
    ),
    versiya="0.2.0",
    baza_api="https://гибдд.рф",
    trebuet_autentifikatsii=False,
    tegi=["гибдд", "мвд", "штрафы", "транспорт", "дтп", "водители"],
)
