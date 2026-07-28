"""Тесты для публичного пространства имён mcp-russia."""

from __future__ import annotations

from pathlib import Path

from mcp_russia import __version__
from mcp_russia.server import mcp, reyestr
from mcp_russia.server import mcp as prezhnyaya_mcp
from mcp_russia.server import reyestr as prezhniy_reyestr


def test_publichnoe_prostranstvo_imen_pereeksportiruet_kornevoy_server() -> None:
    assert mcp is prezhnyaya_mcp
    assert reyestr is prezhniy_reyestr


def test_publichnoe_prostranstvo_imen_otkryvaet_versiyu() -> None:
    assert __version__


def test_metadannye_aktivnyh_moduley_ne_pomecheny_kak_zaglushki() -> None:
    katalog_dannyh = Path(__file__).parents[1] / "src" / "mcp_russia" / "data"
    fayly_metadannyh = (
        *katalog_dannyh.glob("*/prompts.py"),
        *katalog_dannyh.glob("*/resources.py"),
    )

    ustarevshie_pometki = {
        str(fayl.relative_to(katalog_dannyh)): nomer_stroki
        for fayl in fayly_metadannyh
        for nomer_stroki, stroka in enumerate(
            fayl.read_text(encoding="utf-8").splitlines(),
            start=1,
        )
        if "заглушк" in stroka.casefold()
    }

    assert not ustarevshie_pometki, (
        "Публичные промпты и ресурсы активных модулей не должны называться заглушками: "
        f"{ustarevshie_pometki}"
    )
