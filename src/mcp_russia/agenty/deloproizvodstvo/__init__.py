"""Слой генерации официальных документов РФ в mcp-russia.

Модуль предоставляет инструменты для создания официальных документов
(письмо, распоряжение, приказ, акт, справка, протокол, докладная_записка)
на основе ГОСТ Р 7.0.97-2016 и правил делопроизводства РФ.
"""

from mcp_russia._shared.feature import MetaFunktsii

META_FUNKTSII = MetaFunktsii(
    imya="deloproizvodstvo",
    opisanie=(
        "Deloproizvodstvo v mcp-russia: "
        "Ofitsialnaya perepiska RF: pismo, rasporyazhenie, prikaz, akt, spravka "
        "na osnove GOST R 7.0.97-2016 i pravil deloproizvodstva RF"
    ),
    versiya="0.1.0",
    trebuet_autentifikatsii=False,
    tegi=["dokumenty", "deloproizvodstvo", "ofitsialnaya-perepiska"],
)
