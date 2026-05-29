"""Тесты инструментов модуля ФССП."""

from mcp_russia.data.fssp import tools as fssp_tools


def test_spisok_vidov_proizvodstv():
    result = fssp_tools.spisok_vidov_proizvodstv()
    assert isinstance(result, list)
    assert len(result) > 0
    assert any(v["code"] == "shtrafy_gibdd" for v in result)


def test_spisok_statusov_proizvodstva():
    result = fssp_tools.spisok_statusov_proizvodstva()
    assert isinstance(result, list)
    assert any(s["code"] == "v_proizvodstve" for s in result)


def test_spisok_ogranicheniy():
    result = fssp_tools.spisok_ogranicheniy()
    assert isinstance(result, list)
    assert any(o["code"] == "vyezd" for o in result)


def test_spisok_kategoriy_dolzhnikov():
    result = fssp_tools.spisok_kategoriy_dolzhnikov()
    assert isinstance(result, list)
    assert any(k["code"] == "ip" for k in result)


def test_spisok_osnovaniy_vozbuzhdeniya():
    result = fssp_tools.spisok_osnovaniy_vozbuzhdeniya()
    assert isinstance(result, list)
    assert any(o["code"] == "sudebnyy_akt" for o in result)


def test_info_proizvodstva():
    result = fssp_tools.info_proizvodstva("12345/23/77001-ИП")
    assert result["nomer"] == "12345/23/77001-ИП"
    assert "placeholder" in result["status"]


def test_poisk_dolzhnika():
    result = fssp_tools.poisk_dolzhnika("Иванов Иван Иванович")
    assert isinstance(result, list)


def test_ogranicheniya_dolzhnika():
    result = fssp_tools.ogranicheniya_dolzhnika("Иванов Иван Иванович")
    assert isinstance(result, list)


def test_rozysk_dolzhnika():
    result = fssp_tools.rozysk_dolzhnika("Иванов Иван Иванович")
    assert isinstance(result, list)
