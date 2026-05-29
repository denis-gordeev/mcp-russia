"""Росводресурсы — данные Федерального агентства водных ресурсов."""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="rosvodresursy",
    description=(
        "Данные Росводресурсов: водные объекты РФ, бассейновые округа, "
        "уровни воды, гидрологические посты, состояние водохранилищ, "
        "водопользование и водохозяйственные системы"
    ),
    version="0.1.0",
    api_base="https://rosvodresursy.ru",
    requires_auth=False,
    tags=["вода", "гидрология", "водоёмы", "реки", "водохранилища", "росводресурсы"],
)
