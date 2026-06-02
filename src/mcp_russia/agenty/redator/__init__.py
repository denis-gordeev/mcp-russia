"""Russian official document generation layer within mcp-russia.

This module provides tools for generating official Russian documents
(pismo, rasporyazhenie, prikaz, akt, spravka, protokol, dokladnaya_zapiska)
based on Russian official document standards (GOST R 7.0.97-2016,
Deloproizvodstvo RF).
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
