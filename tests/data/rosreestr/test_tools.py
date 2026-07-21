"""Тесты инструментов модуля Росреестра."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosreestr import tools as rre_tools
from mcp_russia.data.rosreestr.schemas import KadastrovayaStoimost, KadastrovyyObekt


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


def test_spisok_tipov_nedvizhimosti():
    rezultat = rre_tools.spisok_tipov_nedvizhimosti()
    assert isinstance(rezultat, list)
    assert len(rezultat) > 0
    assert any(t["kod"] == "zemelnyy_uchastok" for t in rezultat)


def test_spisok_kategoriy_zemel():
    rezultat = rre_tools.spisok_kategoriy_zemel()
    assert isinstance(rezultat, list)
    assert any(k["kod"] == "naselennyh_punktov" for k in rezultat)


def test_spisok_vidov_ispolzovaniya():
    rezultat = rre_tools.spisok_vidov_ispolzovaniya()
    assert isinstance(rezultat, list)
    assert any(v["kod"] == "zhiloe" for v in rezultat)


def test_spisok_statusov_obekta():
    rezultat = rre_tools.spisok_statusov_obekta()
    assert isinstance(rezultat, list)
    assert any(s["kod"] == "uchtenny" for s in rezultat)


def test_spisok_form_sobstvennosti():
    rezultat = rre_tools.spisok_form_sobstvennosti()
    assert isinstance(rezultat, list)
    assert any(f["kod"] == "chastnaya" for f in rezultat)


async def test_info_obekta_uspekh():
    kontekst = _maket_konteksta()
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
            sostoyanie_ucheta="Учтённый",
            kategoriya_zemel="Земли населённых пунктов",
        ),
    ):
        rezultat = await rre_tools.info_obekta("77:01:0001001:1001", kontekst)
    assert "77:01:0001001:1001" in rezultat
    assert "Земельный участок" in rezultat
    assert "pkk.rosreestr.ru" in rezultat


async def test_info_obekta_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(rre_tools.client, "poluchit_obekt", return_value=None):
        rezultat = await rre_tools.info_obekta("00:00:0000000:000", kontekst)
    assert "не найден" in rezultat


async def test_kadastrovaya_stoimost_uspekh():
    kontekst = _maket_konteksta()
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
        rezultat = await rre_tools.kadastrovaya_stoimost("77:01:0001001:1001", kontekst)
    assert "77:01:0001001:1001" in rezultat
    assert "5" in rezultat
    assert "pkk.rosreestr.ru" in rezultat


async def test_kadastrovaya_stoimost_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(rre_tools.client, "poluchit_kadastrovnuyu_stoimost", return_value=None):
        rezultat = await rre_tools.kadastrovaya_stoimost("00:00:0000000:000", kontekst)
    assert "не найден" in rezultat


async def test_prava_na_obekt_uspekh():
    kontekst = _maket_konteksta()
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
        rezultat = await rre_tools.prava_na_obekt("77:01:0001001:1001", kontekst)
    assert "Собственность" in rezultat
    assert "Иванов" in rezultat


async def test_prava_na_obekt_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rre_tools.client, "poluchit_prava", return_value=[]):
        rezultat = await rre_tools.prava_na_obekt("77:01:0001001:1001", kontekst)
    assert "отсутствуют" in rezultat or "ЕГРН" in rezultat
