"""Слой генерации официальных документов РФ в mcp-russia.

Модуль предоставляет инструменты для создания официальных документов
(письмо, распоряжение, приказ, акт, справка, протокол, докладная_записка)
на основе ГОСТ Р 7.0.97-2016 и правил делопроизводства РФ.
"""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="deloproizvodstvo",
    description=(
        "Deloproizvodstvo v mcp-russia: "
        "Ofitsialnaya perepiska RF: pismo, rasporyazhenie, prikaz, akt, spravka "
        "na osnove GOST R 7.0.97-2016 i pravil deloproizvodstva RF"
    ),
    version="0.1.0",
    requires_auth=False,
    tags=["dokumenty", "deloproizvodstvo", "ofitsialnaya-perepiska"],
)
