"""Тесты инструментов модуля Росреестра."""

from mcp_russia.data.rosreestr import tools as rre_tools


def test_spisok_tipov_nedvizhimosti():
    result = rre_tools.spisok_tipov_nedvizhimosti()
    assert isinstance(result, list)
    assert len(result) > 0
    assert any(t["code"] == "zemelnyy_uchastok" for t in result)


def test_spisok_kategoriy_zemel():
    result = rre_tools.spisok_kategoriy_zemel()
    assert isinstance(result, list)
    assert any(k["code"] == "naselennyh_punktov" for k in result)


def test_spisok_vidov_ispolzovaniya():
    result = rre_tools.spisok_vidov_ispolzovaniya()
    assert isinstance(result, list)
    assert any(v["code"] == "zhiloe" for v in result)


def test_spisok_statusov_obiekta():
    result = rre_tools.spisok_statusov_obiekta()
    assert isinstance(result, list)
    assert any(s["code"] == "uchtenny" for s in result)


def test_spisok_form_sobstvennosti():
    result = rre_tools.spisok_form_sobstvennosti()
    assert isinstance(result, list)
    assert any(f["code"] == "chastnaya" for f in result)


def test_info_obekta():
    result = rre_tools.info_obekta("77:01:0001001:1001")
    assert result["kadastrovyy_nomer"] == "77:01:0001001:1001"
    assert "placeholder" in result["status_ucheta"]


def test_kadastrovaya_stoimost():
    result = rre_tools.kadastrovaya_stoimost("77:01:0001001:1001")
    assert result["kadastrovyy_nomer"] == "77:01:0001001:1001"
    assert "placeholder" in result["osnovanie"]


def test_prava_na_obekt():
    result = rre_tools.prava_na_obekt("77:01:0001001:1001")
    assert isinstance(result, list)
