"""Тесты инструментов модуля Росприроднадзор."""

from unittest.mock import AsyncMock, patch

from mcp_russia.data.rosprirodnadzor import tools as rpn_tools


def _maket_konteksta():
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.warning = AsyncMock()
    return ctx


async def test_spisok_vidov_nadzora():
    ctx = _maket_konteksta()
    result = await rpn_tools.spisok_vidov_nadzora(ctx)
    assert "надзор" in result.lower() or "экологический" in result.lower()


async def test_spisok_kategoriy_obnv():
    ctx = _maket_konteksta()
    result = await rpn_tools.spisok_kategoriy_obnv(ctx)
    assert "категория" in result.lower() or "значительн" in result.lower()


async def test_spisok_vidov_litsenziy_nedra():
    ctx = _maket_konteksta()
    result = await rpn_tools.spisok_vidov_litsenziy_nedra(ctx)
    assert "лицензий" in result.lower() or "недр" in result.lower()


async def test_poisk_proverok_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rpn_tools.client, "poisk_proverok", return_value=[]):
        result = await rpn_tools.poisk_proverok(ctx)
    assert isinstance(result, str)


async def test_poisk_proverok_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer": "ПР-2026-001",
            "organizaciya": "ООО «Промышленник»",
            "vid_nadzora": "Государственный экологический надзор",
            "data_nachala": "2026-02-01",
            "data_okonchaniya": "2026-03-01",
            "sostoyanie": "Завершено",
            "vyavleno_narusheniy": 3,
        },
    ]
    with patch.object(rpn_tools.client, "poisk_proverok", return_value=mock_data):
        result = await rpn_tools.poisk_proverok(ctx)
    assert "Промышленник" in result


async def test_info_proverki_ne_nayden():
    ctx = _maket_konteksta()
    with patch.object(rpn_tools.client, "info_proverki", return_value=None):
        result = await rpn_tools.info_proverki("nesushchestvuyushchiy", ctx)
    assert "не найдена" in result


async def test_info_proverki_nayden():
    ctx = _maket_konteksta()
    mock_data = {
        "nomer": "ПР-2026-001",
        "organizaciya": "ООО «Промышленник»",
        "vid_nadzora": "Государственный экологический надзор",
        "data_nachala": "2026-02-01",
        "data_okonchaniya": "2026-03-01",
        "sostoyanie": "Завершено",
        "vyavleno_narusheniy": 3,
    }
    with patch.object(rpn_tools.client, "info_proverki", return_value=mock_data):
        result = await rpn_tools.info_proverki("ПР-2026-001", ctx)
    assert "Промышленник" in result


async def test_poisk_obektov_negativnogo_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rpn_tools.client, "poisk_obektov_negativnogo", return_value=[]):
        result = await rpn_tools.poisk_obektov_negativnogo(ctx)
    assert isinstance(result, str)


async def test_poisk_obektov_negativnogo_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer": "ОНВ-001",
            "nazvanie": "Завод «Химпром»",
            "kategoriya": "I — значительное",
            "subiekt": "Волгоградская область",
            "vid_deyatelnosti": "Химическое производство",
        },
    ]
    with patch.object(rpn_tools.client, "poisk_obektov_negativnogo", return_value=mock_data):
        result = await rpn_tools.poisk_obektov_negativnogo(ctx)
    assert "Химпром" in result


async def test_poisk_litsenziy_nedra_pustoy():
    ctx = _maket_konteksta()
    with patch.object(rpn_tools.client, "poisk_litsenziy_nedra", return_value=[]):
        result = await rpn_tools.poisk_litsenziy_nedra(ctx)
    assert isinstance(result, str)


async def test_poisk_litsenziy_nedra_nayden():
    ctx = _maket_konteksta()
    mock_data = [
        {
            "nomer": "ЛЦ-001",
            "vid_litsenzii": "Добыча полезных ископаемых",
            "territoriya": "ХМАО-Югра",
            "srok_deystviya": "2020–2030",
            "derzhatel": "ПАО «Газпром»",
        },
    ]
    with patch.object(rpn_tools.client, "poisk_litsenziy_nedra", return_value=mock_data):
        result = await rpn_tools.poisk_litsenziy_nedra(ctx)
    assert "Газпром" in result
