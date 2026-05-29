"""Роскомнадзор — данные Федеральной службы по надзору в сфере связи,
информационных технологий и массовых коммуникаций."""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="roskomnadzor",
    description=(
        "Данные Роскомнадзора: реестры запрещённых сайтов, операторы "
        "персональных данных, лицензии связи, СМИ, нарушения в сфере ИТ"
    ),
    version="0.1.0",
    api_base="https://rkn.gov.ru",
    requires_auth=False,
    tags=["роскомнадзор", "связь", "сми", "персональные-данные", "реестр"],
)
