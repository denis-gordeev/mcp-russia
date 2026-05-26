"""Тесты инструментов модуля Роскомнадзора."""

from mcp_brasil.data.roskomnadzor import tools as rkn_tools


def test_spisok_napravleniy():
    result = rkn_tools.spisok_napravleniy()
    assert isinstance(result, list)
    assert len(result) > 0
    assert any(n["code"] == "media_supervision" for n in result)


def test_spisok_tipov_licenziy():
    result = rkn_tools.spisok_tipov_licenziy()
    assert isinstance(result, list)
    assert any(t["code"] == "internet" for t in result)


def test_spisok_kategoriy_narusheniy():
    result = rkn_tools.spisok_kategoriy_narusheniy()
    assert isinstance(result, list)
    assert any(k["code"] == "personal_data_leak" for k in result)


def test_spisok_reestrov():
    result = rkn_tools.spisok_reestrov()
    assert isinstance(result, list)
    assert any(r["code"] == "blocked_sites" for r in result)


def test_spisok_tipov_smi():
    result = rkn_tools.spisok_tipov_smi()
    assert isinstance(result, list)
    assert any(t["code"] == "online" for t in result)


def test_spisok_kategoriy_pd_operatorov():
    result = rkn_tools.spisok_kategoriy_pd_operatorov()
    assert isinstance(result, list)
    assert any(k["code"] == "commercial" for k in result)


def test_info_licenzii():
    result = rkn_tools.info_licenzii("LIC-001")
    assert result["nomer"] == "LIC-001"
    assert "placeholder" in result["status"]


def test_poisk_smi():
    result = rkn_tools.poisk_smi()
    assert isinstance(result, list)


def test_info_operatora_pd():
    result = rkn_tools.info_operatora_pd()
    assert isinstance(result, list)


def test_poisk_narusheniy():
    result = rkn_tools.poisk_narusheniy()
    assert isinstance(result, list)


def test_zapisi_reestra():
    result = rkn_tools.zapisi_reestra("blocked_sites")
    assert isinstance(result, list)
