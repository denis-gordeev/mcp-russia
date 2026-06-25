"""Росводресурсы — данные Федерального агентства водных ресурсов."""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="rosvodresursy",
    opisanie=(
        "Данные Росводресурсов: водные объекты РФ, бассейновые округа, "
        "уровни воды, гидрологические посты, состояние водохранилищ, "
        "водопользование и водохозяйственные системы"
    ),
    versiya="0.2.0",
    baza_api="https://rosvodresursy.ru",
    trebuet_autentifikatsii=False,
    tegi=["вода", "гидрология", "водоёмы", "реки", "водохранилища", "росводресурсы"],
)
