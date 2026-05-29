"""Тесты инструментов модуля Роспотребнадзора."""

from mcp_russia.data.rospotrebnadzor import tools as rpn_tools


def test_spisok_napravleniy():
    result = rpn_tools.spisok_napravleniy()
    assert isinstance(result, list)
    assert len(result) > 0
    assert any(n["code"] == "sanitary" for n in result)


def test_spisok_tipov_proverok():
    result = rpn_tools.spisok_tipov_proverok()
    assert isinstance(result, list)
    assert any(t["code"] == "planovaya" for t in result)


def test_spisok_kategoriy_obiektov():
    result = rpn_tools.spisok_kategoriy_obiektov()
    assert isinstance(result, list)
    assert any(k["code"] == "food_enterprise" for k in result)


def test_spisok_regionalnyh_upravleniy():
    result = rpn_tools.spisok_regionalnyh_upravleniy()
    assert isinstance(result, list)
    assert any(r["code"] == "CFD" for r in result)


def test_info_proverki():
    result = rpn_tools.info_proverki("12345")
    assert result["nomer"] == "12345"
    assert "placeholder" in result["status"]


def test_poisk_narusheniy():
    result = rpn_tools.poisk_narusheniy()
    assert isinstance(result, list)


def test_spisok_sanpinov():
    result = rpn_tools.spisok_sanpinov()
    assert isinstance(result, list)
    assert any(s["code"] == "2.1.3684-21" for s in result)


def test_zhaloby_potrebiteley():
    result = rpn_tools.zhaloby_potrebiteley()
    assert isinstance(result, list)


def test_pokazateli_bezopasnosti():
    result = rpn_tools.pokazateli_bezopasnosti()
    assert isinstance(result, list)
