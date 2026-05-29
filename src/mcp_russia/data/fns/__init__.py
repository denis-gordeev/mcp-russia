"""ФНС — данные Федеральной налоговой службы."""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="fns",
    description=(
        "Данные ФНС России: налоговые начисления, проверки, ЕГРЮЛ/ЕГРИП, "
        "сведения об организациях и ИП, налоговые ставки и режимы"
    ),
    version="0.1.0",
    api_base="https://api.nalog.ru",
    requires_auth=False,
    tags=["фнс", "налоги", "егрюл", "проверки", "бизнес"],
)
