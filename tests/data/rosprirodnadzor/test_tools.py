"""Тесты инструментов модуля Росприроднадзор."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosprirodnadzor import tools as rpn_tools


def _maket_konteksta():
    kontekst = AsyncMock()
    kontekst.info = AsyncMock()
    kontekst.warning = AsyncMock()
    return kontekst


async def test_spisok_vidov_nadzora():
    kontekst = _maket_konteksta()
    rezultat = await rpn_tools.spisok_vidov_nadzora(kontekst)
    assert "надзор" in rezultat.lower() or "экологический" in rezultat.lower()


async def test_spisok_kategoriy_obnv():
    kontekst = _maket_konteksta()
    rezultat = await rpn_tools.spisok_kategoriy_obnv(kontekst)
    assert "категория" in rezultat.lower() or "значительн" in rezultat.lower()


async def test_spisok_vidov_litsenziy_nedra():
    kontekst = _maket_konteksta()
    rezultat = await rpn_tools.spisok_vidov_litsenziy_nedra(kontekst)
    assert "лицензий" in rezultat.lower() or "недр" in rezultat.lower()


async def test_poisk_proverok_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rpn_tools.client, "poisk_proverok", return_value=[]):
        rezultat = await rpn_tools.poisk_proverok(kontekst)
    assert isinstance(rezultat, str)


async def test_poisk_proverok_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "ПР-2026-001",
            "organizatsiya": "ООО «Промышленник»",
            "vid_nadzora": "Государственный экологический надзор",
            "data_nachala": "2026-02-01",
            "data_okonchaniya": "2026-03-01",
            "sostoyanie": "Завершено",
            "vyavleno_narusheniy": 3,
        },
    ]
    with patch.object(rpn_tools.client, "poisk_proverok", return_value=maket_dannykh):
        rezultat = await rpn_tools.poisk_proverok(kontekst)
    assert "Промышленник" in rezultat


async def test_info_proverki_ne_nayden():
    kontekst = _maket_konteksta()
    with patch.object(rpn_tools.client, "info_proverki", return_value=None):
        rezultat = await rpn_tools.info_proverki("nesushchestvuyushchiy", kontekst)
    assert "не найдена" in rezultat


async def test_info_proverki_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = {
        "nomer": "ПР-2026-001",
        "organizatsiya": "ООО «Промышленник»",
        "vid_nadzora": "Государственный экологический надзор",
        "data_nachala": "2026-02-01",
        "data_okonchaniya": "2026-03-01",
        "sostoyanie": "Завершено",
        "vyavleno_narusheniy": 3,
    }
    with patch.object(rpn_tools.client, "info_proverki", return_value=maket_dannykh):
        rezultat = await rpn_tools.info_proverki("ПР-2026-001", kontekst)
    assert "Промышленник" in rezultat


async def test_poisk_obektov_negativnogo_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rpn_tools.client, "poisk_obektov_negativnogo", return_value=[]):
        rezultat = await rpn_tools.poisk_obektov_negativnogo(kontekst)
    assert isinstance(rezultat, str)


async def test_poisk_obektov_negativnogo_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "ОНВ-001",
            "nazvanie": "Завод «Химпром»",
            "kategoriya": "I — значительное",
            "subiekt": "Волгоградская область",
            "vid_deyatelnosti": "Химическое производство",
        },
    ]
    with patch.object(rpn_tools.client, "poisk_obektov_negativnogo", return_value=maket_dannykh):
        rezultat = await rpn_tools.poisk_obektov_negativnogo(kontekst)
    assert "Химпром" in rezultat


async def test_poisk_litsenziy_nedra_pustoy():
    kontekst = _maket_konteksta()
    with patch.object(rpn_tools.client, "poisk_litsenziy_nedra", return_value=[]):
        rezultat = await rpn_tools.poisk_litsenziy_nedra(kontekst)
    assert isinstance(rezultat, str)


async def test_poisk_litsenziy_nedra_nayden():
    kontekst = _maket_konteksta()
    maket_dannykh = [
        {
            "nomer": "ЛЦ-001",
            "vid_litsenzii": "Добыча полезных ископаемых",
            "territoriya": "ХМАО-Югра",
            "srok_deystviya": "2020–2030",
            "derzhatel": "ПАО «Газпром»",
        },
    ]
    with patch.object(rpn_tools.client, "poisk_litsenziy_nedra", return_value=maket_dannykh):
        rezultat = await rpn_tools.poisk_litsenziy_nedra(kontekst)
    assert "Газпром" in rezultat
