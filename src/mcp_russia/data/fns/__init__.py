"""ФНС — данные Федеральной налоговой службы."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="fns",
    opisanie=(
        "Данные ФНС России: налоговые начисления, проверки, ЕГРЮЛ/ЕГРИП, "
        "сведения об организациях и ИП, налоговые ставки и режимы"
    ),
    versiya="0.2.0",
    baza_api="https://egrul.nalog.ru",
    trebuet_autentifikatsii=False,
    tegi=["фнс", "налоги", "егрюл", "проверки", "бизнес"],
)
