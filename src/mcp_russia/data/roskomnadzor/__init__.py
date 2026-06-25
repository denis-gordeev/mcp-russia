"""Роскомнадзор — данные Федеральной службы по надзору в сфере связи,
информационных технологий и массовых коммуникаций."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="roskomnadzor",
    opisanie=(
        "Данные Роскомнадзора: реестры запрещённых сайтов, операторы "
        "персональных данных, лицензии связи, СМИ, нарушения в сфере ИТ"
    ),
    versiya="0.2.0",
    baza_api="https://rkn.gov.ru",
    trebuet_autentifikatsii=False,
    tegi=["роскомнадзор", "связь", "сми", "персональные-данные", "реестр"],
)
