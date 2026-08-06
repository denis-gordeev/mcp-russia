"""Тесты инструментов модуля Ростехнадзора."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rostekhnadzor import constants as rt_constants
from mcp_russia.data.rostekhnadzor import tools as rt_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_vidov_nadzora():
    kontekst = _maket_konteksta()
    rezultat = await rt_tools.spisok_vidov_nadzora(kontekst)
    assert "Промышленн" in rezultat or "Атомн" in rezultat


async def test_spisok_klassov_opasnosti():
    kontekst = _maket_konteksta()
    rezultat = await rt_tools.spisok_klassov_opasnosti(kontekst)
    assert "особо опасн" in rezultat.lower() or "I класс" in rezultat


async def test_spisok_vidov_litsenziy():
    kontekst = _maket_konteksta()
    rezultat = await rt_tools.spisok_vidov_litsenziy(kontekst)
    assert "Эксплуатац" in rezultat or "Проектиров" in rezultat


async def test_spisok_vidov_intsidentov():
    kontekst = _maket_konteksta()
    rezultat = await rt_tools.spisok_vidov_intsidentov(kontekst)
    assert "Авари" in rezultat or "Инцидент" in rezultat


async def test_poisk_intsidentov_zapasnoy():
    kontekst = _maket_konteksta()
    with patch.object(rt_tools.client, "poisk_intsidentov", return_value=[]):
        rezultat = await rt_tools.poisk_intsidentov(kontekst)
    assert "2024" in rezultat or "резервные данные" in rezultat or "rostechnadzor" in rezultat


async def test_poisk_intsidentov_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "И-2024-001",
            "vid": "Авария",
            "data": "2024-03-15",
            "subiekt": "Свердловская область",
            "opisanie": "Разрушение оборудования на химическом заводе",
            "pogibshikh": 0,
            "postradavshikh": 3,
        },
    ]
    with patch.object(rt_tools.client, "poisk_intsidentov", return_value=maket_dannykh):
        rezultat = await rt_tools.poisk_intsidentov(kontekst)
    assert "Свердловск" in rezultat


async def test_poisk_litsenziy_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rt_tools.client, "poisk_litsenziy", return_value=[]):
        rezultat = await rt_tools.poisk_litsenziy(kontekst)
    assert isinstance(rezultat, str)


async def test_poisk_litsenziy_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "Л-001234",
            "vid": "Эксплуатация ОПО",
            "organizatsiya": "ООО «ХимПром»",
            "subiekt": "Нижегородская область",
            "data_vydachi": "2020-06-15",
            "srok_deystviya": "2025-06-15",
            "sostoyanie": "Действует",
        },
    ]
    with patch.object(rt_tools.client, "poisk_litsenziy", return_value=maket_dannykh):
        rezultat = await rt_tools.poisk_litsenziy(kontekst)
    assert "ХимПром" in rezultat


async def test_reestr_opo_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rt_tools.client, "reestr_opo", return_value=[]):
        rezultat = await rt_tools.reestr_opo(kontekst)
    assert isinstance(rezultat, str)


async def test_reestr_opo_s_dannymi():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "registratsionnyy_nomer": "ОПО-001-12345",
            "nazvanie": "Нефтеперерабатывающий завод",
            "vid_deyatelnosti": "Переработка нефти",
            "klass_opasnosti": "II класс",
            "subiekt": "Самарская область",
            "organizatsiya": "ПАО «Нефть»",
        },
    ]
    with patch.object(rt_tools.client, "reestr_opo", return_value=maket_dannykh):
        rezultat = await rt_tools.reestr_opo(kontekst)
    assert "Нефтеперерабат" in rezultat


def test_constants_vidy_nadzora():
    assert len(rt_constants.VIDY_NADZORA) == 6


def test_constants_klassy_opasnosti():
    assert len(rt_constants.KLASSY_OPASNOSTI) == 4


def test_constants_vidy_litsenziy():
    assert len(rt_constants.VIDY_LITSENZIY) == 9


def test_constants_vidy_intsidentov():
    assert len(rt_constants.VIDY_INTSIDENTOV) == 6


def test_constants_statistika_prombez():
    s = rt_constants.STATISTIKA_PROMBEZ_2024
    assert s["vsego_avariy"] > 0
    assert len(s["po_vidu_nadzora"]) == 4
