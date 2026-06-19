"""Тесты инструментов модуля ФНС."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.fns import tools as fns_tools
from mcp_russia.data.fns.schemas import IPEGRIP, OrganizaciyaEGRUL


def _mock_ctx():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


def test_spisok_nalogovyh_rezhimov():
    result = fns_tools.spisok_nalogovyh_rezhimov()
    assert isinstance(result, list)
    assert len(result) > 0
    assert any(r["kod"] == "osno" for r in result)


def test_spisok_vidov_nalogov():
    result = fns_tools.spisok_vidov_nalogov()
    assert isinstance(result, list)
    assert any(v["kod"] == "nds" for v in result)


def test_spisok_tipov_proverok():
    result = fns_tools.spisok_tipov_proverok()
    assert isinstance(result, list)
    assert any(t["kod"] == "kameralnaya" for t in result)


def test_spisok_statusov_organizaciy():
    result = fns_tools.spisok_statusov_organizaciy()
    assert isinstance(result, list)
    assert any(s["kod"] == "deystvuyushchaya" for s in result)


def test_spisok_kategoriy_nalogoplatelshchikov():
    result = fns_tools.spisok_kategoriy_nalogoplatelshchikov()
    assert isinstance(result, list)
    assert any(k["kod"] == "ip" for k in result)


async def test_info_organizacii_found():
    ctx = _mock_ctx()
    mock_org = OrganizaciyaEGRUL(
        inn="7707083893",
        ogrn="1027700132195",
        nazvanie="ПАО Сбербанк",
        polnoe_nazvanie="Публичное акционерное общество Сбербанк России",
        yuridicheskiy_adres="г. Москва, ул. Вавилова, д. 19",
        data_registracii="2002-08-22",
        status="Действующая",
    )
    with patch.object(fns_tools.client, "poluchit_organizaciyu", return_value=mock_org):
        result = await fns_tools.info_organizacii("7707083893", ctx=ctx)
    assert "7707083893" in result
    assert "ПАО Сбербанк" in result
    assert "Действующая" in result


async def test_info_organizacii_not_found():
    ctx = _mock_ctx()
    with patch.object(fns_tools.client, "poluchit_organizaciyu", return_value=None):
        result = await fns_tools.info_organizacii("0000000000", ctx=ctx)
    assert "не найдена" in result


async def test_info_ip_found():
    ctx = _mock_ctx()
    mock_ip = IPEGRIP(
        inn="500100732259",
        ogrnip="304500116000157",
        fio="Иванов Иван Иванович",
        data_registracii="2004-04-27",
        status="Действующая",
    )
    with patch.object(fns_tools.client, "poluchit_ip", return_value=mock_ip):
        result = await fns_tools.info_ip("500100732259", ctx=ctx)
    assert "500100732259" in result
    assert "Иванов" in result


async def test_info_ip_not_found():
    ctx = _mock_ctx()
    with patch.object(fns_tools.client, "poluchit_ip", return_value=None):
        result = await fns_tools.info_ip("000000000000", ctx=ctx)
    assert "не найден" in result


async def test_proverki_organizacii():
    ctx = _mock_ctx()
    with patch.object(fns_tools.client, "poluchit_proverki", return_value=[]):
        result = await fns_tools.proverki_organizacii("7707083893", ctx=ctx)
    assert "недоступны" in result


async def test_nalogovye_nachisleniya():
    ctx = _mock_ctx()
    with patch.object(fns_tools.client, "poluchit_nachisleniya", return_value=[]):
        result = await fns_tools.nalogovye_nachisleniya("7707083893", ctx=ctx)
    assert "недоступны" in result
