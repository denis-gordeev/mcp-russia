"""Минобрнауки — данные Министерства науки и высшего образования РФ."""

from mcp_russia._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="minobrnauki",
    description=(
        "Данные Минобрнауки России: вузы, научные исследования, "
        "образовательные программы, рейтинги, гранты, аспирантура"
    ),
    version="0.2.0",
    api_base="https://obrnadzor.gov.ru",
    requires_auth=False,
    tags=["минобрнауки", "образование", "наука", "вузы", "исследования"],
)
