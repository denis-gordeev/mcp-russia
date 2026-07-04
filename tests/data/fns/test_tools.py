"""Тесты инструментов модуля ФНС."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.fns import tools as fns_tools
from mcp_russia.data.fns.schemas import IPEGRIP, OrganizaciyaEGRUL


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


def test_spisok_nalogovyh_rezhimov():
    rezultat = fns_tools.spisok_nalogovyh_rezhimov()
    assert isinstance(rezultat, list)
    assert len(rezultat) > 0
    assert any(r["kod"] == "osno" for r in rezultat)


def test_spisok_vidov_nalogov():
    rezultat = fns_tools.spisok_vidov_nalogov()
    assert isinstance(rezultat, list)
    assert any(v["kod"] == "nds" for v in rezultat)


def test_spisok_tipov_proverok():
    rezultat = fns_tools.spisok_tipov_proverok()
    assert isinstance(rezultat, list)
    assert any(t["kod"] == "kameralnaya" for t in rezultat)


def test_spisok_statusov_organizaciy():
    rezultat = fns_tools.spisok_statusov_organizaciy()
    assert isinstance(rezultat, list)
    assert any(s["kod"] == "deystvuyushchaya" for s in rezultat)


def test_spisok_kategoriy_nalogoplatelshchikov():
    rezultat = fns_tools.spisok_kategoriy_nalogoplatelshchikov()
    assert isinstance(rezultat, list)
    assert any(k["kod"] == "ip" for k in rezultat)


async def test_info_organizacii_nayden():
    ctx = _maket_konteksta()
    maket_organizatsii = OrganizaciyaEGRUL(
        inn="7707083893",
        ogrn="1027700132195",
        nazvanie="ПАО Сбербанк",
        polnoe_nazvanie="Публичное акционерное общество Сбербанк России",
        yuridicheskiy_adres="г. Москва, ул. Вавилова, д. 19",
        data_registracii="2002-08-22",
        sostoyanie="Действующая",
    )
    with patch.object(fns_tools.client, "poluchit_organizaciyu", return_value=maket_organizatsii):
        rezultat = await fns_tools.info_organizacii("7707083893", ctx=ctx)
    assert "7707083893" in rezultat
    assert "ПАО Сбербанк" in rezultat
    assert "Действующая" in rezultat


async def test_info_organizacii_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(fns_tools.client, "poluchit_organizaciyu", return_value=None):
        rezultat = await fns_tools.info_organizacii("0000000000", ctx=ctx)
    assert "не найдена" in rezultat


async def test_info_ip_nayden():
    ctx = _maket_konteksta()
    maket_ip = IPEGRIP(
        inn="500100732259",
        ogrnip="304500116000157",
        fio="Иванов Иван Иванович",
        data_registracii="2004-04-27",
        sostoyanie="Действующая",
    )
    with patch.object(fns_tools.client, "poluchit_ip", return_value=maket_ip):
        rezultat = await fns_tools.info_ip("500100732259", ctx=ctx)
    assert "500100732259" in rezultat
    assert "Иванов" in rezultat


async def test_info_ip_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(fns_tools.client, "poluchit_ip", return_value=None):
        rezultat = await fns_tools.info_ip("000000000000", ctx=ctx)
    assert "не найден" in rezultat


async def test_proverki_organizacii():
    ctx = _maket_konteksta()
    with patch.object(fns_tools.client, "poluchit_proverki", return_value=[]):
        rezultat = await fns_tools.proverki_organizacii("7707083893", ctx=ctx)
    assert "недоступны" in rezultat


async def test_nalogovye_nachisleniya():
    ctx = _maket_konteksta()
    with patch.object(fns_tools.client, "poluchit_nachisleniya", return_value=[]):
        rezultat = await fns_tools.nalogovye_nachisleniya("7707083893", ctx=ctx)
    assert "недоступны" in rezultat
