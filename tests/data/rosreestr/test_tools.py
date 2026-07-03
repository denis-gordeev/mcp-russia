"""Тесты инструментов модуля Росреестра."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosreestr import tools as rre_tools
from mcp_russia.data.rosreestr.schemas import KadastrovayaStoimost, KadastrovyyObekt


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


def test_spisok_tipov_nedvizhimosti():
    result = rre_tools.spisok_tipov_nedvizhimosti()
    assert isinstance(result, list)
    assert len(result) > 0
    assert any(t["kod"] == "zemelnyy_uchastok" for t in result)


def test_spisok_kategoriy_zemel():
    result = rre_tools.spisok_kategoriy_zemel()
    assert isinstance(result, list)
    assert any(k["kod"] == "naselennyh_punktov" for k in result)


def test_spisok_vidov_ispolzovaniya():
    result = rre_tools.spisok_vidov_ispolzovaniya()
    assert isinstance(result, list)
    assert any(v["kod"] == "zhiloe" for v in result)


def test_spisok_statusov_obiekta():
    result = rre_tools.spisok_statusov_obiekta()
    assert isinstance(result, list)
    assert any(s["kod"] == "uchtenny" for s in result)


def test_spisok_form_sobstvennosti():
    result = rre_tools.spisok_form_sobstvennosti()
    assert isinstance(result, list)
    assert any(f["kod"] == "chastnaya" for f in result)


async def test_info_obekta_uspekh():
    ctx = _maket_konteksta()
    with patch.object(
        rre_tools.client,
        "poluchit_obekt",
        return_value=KadastrovyyObekt(
            kadastrovyy_nomer="77:01:0001001:1001",
            tip_obekta="zemelnyy_uchastok",
            adreshnye_svedeniya="г Москва, ул Примерная",
            ploshchad="1000",
            kadastrovaya_stoimost="5000000",
            data_opredeleniya_stoimosti="2024-01-01",
            status_ucheta="Учтённый",
            kategoriya_zemel="Земли населённых пунктов",
        ),
    ):
        result = await rre_tools.info_obekta("77:01:0001001:1001", ctx)
    assert "77:01:0001001:1001" in result
    assert "Земельный участок" in result
    assert "pkk.rosreestr.ru" in result


async def test_info_obekta_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(rre_tools.client, "poluchit_obekt", return_value=None):
        result = await rre_tools.info_obekta("00:00:0000000:000", ctx)
    assert "не найден" in result


async def test_kadastrovaya_stoimost_uspekh():
    ctx = _maket_konteksta()
    with patch.object(
        rre_tools.client,
        "poluchit_kadastrovnuyu_stoimost",
        return_value=KadastrovayaStoimost(
            kadastrovyy_nomer="77:01:0001001:1001",
            stoimost=5000000.0,
            data_opredeleniya="2024-01-01",
            data_vneseniya_v_egrn="2024-01-15",
            osnovanie="Определена в порядке массовой оценки",
        ),
    ):
        result = await rre_tools.kadastrovaya_stoimost("77:01:0001001:1001", ctx)
    assert "77:01:0001001:1001" in result
    assert "5" in result
    assert "pkk.rosreestr.ru" in result


async def test_kadastrovaya_stoimost_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(rre_tools.client, "poluchit_kadastrovnuyu_stoimost", return_value=None):
        result = await rre_tools.kadastrovaya_stoimost("00:00:0000000:000", ctx)
    assert "не найден" in result


async def test_prava_na_obekt_uspekh():
    ctx = _maket_konteksta()
    with patch.object(
        rre_tools.client,
        "poluchit_prava",
        return_value=[
            {
                "tip_prava": "Собственность",
                "sobstvennik": "Иванов И.И.",
                "data_registratsii": "2020-01-01",
                "nomer_registratsii": "77-77/001/2020-001",
            }
        ],
    ):
        result = await rre_tools.prava_na_obekt("77:01:0001001:1001", ctx)
    assert "Собственность" in result
    assert "Иванов" in result


async def test_prava_na_obekt_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rre_tools.client, "poluchit_prava", return_value=[]):
        result = await rre_tools.prava_na_obekt("77:01:0001001:1001", ctx)
    assert "отсутствуют" in result or "ЕГРН" in result
