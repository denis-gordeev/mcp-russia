"""МВД России — данные Министерства внутренних дел Российской Федерации."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="mvd",
    opisanie=(
        "Данные МВД России: статистика преступности, ДТП, розыск, "
        "наркотические преступления, государственный контроль, лицензирование"
    ),
    versiya="0.2.0",
    baza_api="https://мвд.рф",
    trebuet_autentifikatsii=False,
    tegi=[
        "преступность",
        "дтп",
        "розыск",
        "статистика",
        "государственный-контроль",
        "мвд",
    ],
)
