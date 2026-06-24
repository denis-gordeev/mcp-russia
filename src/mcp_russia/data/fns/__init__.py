"""ФНС — данные Федеральной налоговой службы."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    name="fns",
    description=(
        "Данные ФНС России: налоговые начисления, проверки, ЕГРЮЛ/ЕГРИП, "
        "сведения об организациях и ИП, налоговые ставки и режимы"
    ),
    version="0.2.0",
    api_base="https://egrul.nalog.ru",
    requires_auth=False,
    tags=["фнс", "налоги", "егрюл", "проверки", "бизнес"],
)
