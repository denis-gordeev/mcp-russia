"""Тесты инструментов модуля ФНС."""

from mcp_brasil.data.fns import tools as fns_tools


def test_spisok_nalogovyh_rezhimov():
    result = fns_tools.spisok_nalogovyh_rezhimov()
    assert isinstance(result, list)
    assert len(result) > 0
    assert any(r["code"] == "osno" for r in result)


def test_spisok_vidov_nalogov():
    result = fns_tools.spisok_vidov_nalogov()
    assert isinstance(result, list)
    assert any(v["code"] == "nds" for v in result)


def test_spisok_tipov_proverok():
    result = fns_tools.spisok_tipov_proverok()
    assert isinstance(result, list)
    assert any(t["code"] == "kameralnaya" for t in result)


def test_spisok_statusov_organizaciy():
    result = fns_tools.spisok_statusov_organizaciy()
    assert isinstance(result, list)
    assert any(s["code"] == "deystvuyushchaya" for s in result)


def test_spisok_kategoriy_nalogoplatelshchikov():
    result = fns_tools.spisok_kategoriy_nalogoplatelshchikov()
    assert isinstance(result, list)
    assert any(k["code"] == "ip" for k in result)


def test_info_organizacii():
    result = fns_tools.info_organizacii("7707083893")
    assert result["inn"] == "7707083893"
    assert "placeholder" in result["status"]


def test_info_ip():
    result = fns_tools.info_ip("500100732259")
    assert result["inn"] == "500100732259"
    assert "placeholder" in result["status"]


def test_proverki_organizacii():
    result = fns_tools.proverki_organizacii("7707083893")
    assert isinstance(result, list)


def test_nalogovye_nachisleniya():
    result = fns_tools.nalogovye_nachisleniya("7707083893")
    assert isinstance(result, list)
